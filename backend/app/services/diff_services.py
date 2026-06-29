import difflib

def create_diff(
    original_text,
    rewritten_text
):
    
    diff = difflib.ndiff(
        original_text.splitlines(),
        rewritten_text.splitlines()
    )
    
    return list(diff)