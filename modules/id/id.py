def toLean(l): 
    s= l 
    s+= "\n"
    s = s.replace(r"\R", "ℝ")
    s = s.replace(r"\Z", "ℤ")
    s = s.replace(r"\N", "ℕ")  
    return s