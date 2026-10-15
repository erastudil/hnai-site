//! linkcheck : scan site html for github.com/erastudil/<repo> links.
//!
//! offline gate : fail when a linked repo name appears in archived.txt.
//!
//! live gate : with --live, query `gh api repos/erastudil/<repo>`; fail when the repo
//! answers archived, private, or absent.
//!
//! exit code : 0 when every link live; 1 on any dead link; 2 on io or usage fault.

use std::collections::{BTreeMap, BTreeSet};
use std::fs;
use std::path::{Path, PathBuf};
use std::process::{Command, ExitCode};

const OWNER: &str = "erastudil";
const SKIP_DIRS: &[&str] = &[".git", "tools", "node_modules", "target", ".vercel"];

fn main() -> ExitCode {
    let mut live = false;
    let mut root: Option<PathBuf> = None;
    for arg in std::env::args().skip(1) {
        match arg.as_str() {
            "--live" => live = true,
            a if a.starts_with("--") => {
                eprintln!("usage : linkcheck [--live] [site-root]");
                return ExitCode::from(2);
            }
            a => root = Some(PathBuf::from(a)),
        }
    }
    let manifest = Path::new(env!("CARGO_MANIFEST_DIR"));
    let root = root.unwrap_or_else(|| manifest.join("..").join(".."));
    let deny_path = manifest.join("archived.txt");

    let deny = match fs::read_to_string(&deny_path) {
        Ok(s) => s
            .lines()
            .map(str::trim)
            .filter(|l| !l.is_empty() && !l.starts_with('#'))
            .map(str::to_ascii_lowercase)
            .collect::<BTreeSet<_>>(),
        Err(e) => {
            eprintln!("ERROR : read {} : {e}", deny_path.display());
            return ExitCode::from(2);
        }
    };

    let mut html = Vec::new();
    if let Err(e) = collect_html(&root, &mut html) {
        eprintln!("ERROR : walk {} : {e}", root.display());
        return ExitCode::from(2);
    }
    html.sort();

    // repo name (lowercase) -> sites "file:line"
    let mut links: BTreeMap<String, Vec<String>> = BTreeMap::new();
    for file in &html {
        let text = match fs::read_to_string(file) {
            Ok(t) => t,
            Err(e) => {
                eprintln!("ERROR : read {} : {e}", file.display());
                return ExitCode::from(2);
            }
        };
        let rel = file.strip_prefix(&root).unwrap_or(file).display().to_string();
        for (lineno, line) in text.lines().enumerate() {
            for repo in repos_in_line(line) {
                links
                    .entry(repo.to_ascii_lowercase())
                    .or_default()
                    .push(format!("{rel}:{}", lineno + 1));
            }
        }
    }

    println!("html files : {}", html.len());
    println!("deny list : {} names", deny.len());
    println!("linked {OWNER} repos : {}", links.len());

    let mut dead = 0usize;
    for (repo, sites) in &links {
        let verdict = if deny.contains(repo) {
            Err("archived deny list".to_string())
        } else if live {
            live_state(repo)
        } else {
            Ok("deny list clear")
        };
        match verdict {
            Ok(note) => println!("live : {repo} : {note} : {} refs", sites.len()),
            Err(why) => {
                dead += 1;
                println!("DEAD : {repo} : {why} : {}", sites.join(", "));
            }
        }
    }

    if dead == 0 {
        println!("result : every link live; mode {}", if live { "deny list + gh live" } else { "deny list" });
        ExitCode::SUCCESS
    } else {
        println!("result : {dead} dead repo links");
        ExitCode::from(1)
    }
}

fn collect_html(dir: &Path, out: &mut Vec<PathBuf>) -> std::io::Result<()> {
    for entry in fs::read_dir(dir)? {
        let entry = entry?;
        let path = entry.path();
        let name = entry.file_name();
        let name = name.to_string_lossy();
        if entry.file_type()?.is_dir() {
            if !SKIP_DIRS.contains(&name.as_ref()) {
                collect_html(&path, out)?;
            }
        } else if name.to_ascii_lowercase().ends_with(".html") {
            out.push(path);
        }
    }
    Ok(())
}

/// repo names following `github.com/erastudil/` in one line; `.git` suffix stripped.
fn repos_in_line(line: &str) -> Vec<String> {
    let needle = format!("github.com/{OWNER}/");
    let lower = line.to_ascii_lowercase();
    let mut out = Vec::new();
    let mut from = 0;
    while let Some(pos) = lower[from..].find(&needle) {
        let start = from + pos + needle.len();
        let end = line[start..]
            .find(|c: char| !(c.is_ascii_alphanumeric() || c == '-' || c == '_' || c == '.'))
            .map_or(line.len(), |i| start + i);
        let mut name = line[start..end].trim_end_matches('.');
        if let Some(stem) = name.strip_suffix(".git") {
            name = stem;
        }
        if !name.is_empty() {
            out.push(name.to_string());
        }
        from = end.max(start);
    }
    out
}

fn live_state(repo: &str) -> Result<&'static str, String> {
    let out = Command::new("gh")
        .args(["api", &format!("repos/{OWNER}/{repo}"), "--jq", "[.archived,.private]|@tsv"])
        .output()
        .map_err(|e| format!("gh spawn failed : {e}"))?;
    if !out.status.success() {
        return Err(format!("gh api exit {} : repo absent or unreachable", out.status.code().unwrap_or(-1)));
    }
    let s = String::from_utf8_lossy(&out.stdout);
    let mut f = s.trim().split('\t');
    match (f.next(), f.next()) {
        (Some("false"), Some("false")) => Ok("gh public, unarchived"),
        (Some("true"), _) => Err("gh reports archived".into()),
        (_, Some("true")) => Err("gh reports private".into()),
        _ => Err(format!("gh unparsed reply : {}", s.trim())),
    }
}
