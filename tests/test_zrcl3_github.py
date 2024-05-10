
import os


def test_github_release():
    import zrcl3_uses.github as github
    release = github.github_release_meta("bitwarden/clients", "CLI", match="startswith")
    if not os.path.exists("bw.zip"):
        github.download_release(release, filename="bw-windows.*\.zip", match="glob", save="bw.zip")
    if not os.path.exists("bw.sha256"):
        github.download_release(release, filename="bw-windows-sha256.*\.txt", match="glob", save="bw.sha256")

    import zrcl4.hashlib as hashlib
    w : str = hashlib.hash_file("bw.zip")
    assert w.upper() == open("bw.sha256", "r").read().strip()
    
