'''


x := 1


if x = 1 then 
  y := 2 
else 
  y := 3
end


while x < 10 do 
  x := x + 1
end


x := 1; 
y := 2

eg

n := 5;
p := 1;
while n > 0 do
  p := p * n;
  n := n - 1
end
'''
import sys
import re
 
def lex(characters, token_exprs):
    pos = 0
    tokens = []
    while pos < len(characters):
        match = None
        for token_expr in token_exprs:
            pattern, tag = token_expr
            regex = re.compile(pattern)
            match = regex.match(characters, pos)
            if match:
                text = match.group(0)
                if tag:
                    token = (text, tag)
                    tokens.append(token)
                break
        if not match:
            sys.stderr.write('Illegal character: %sn' % characters[pos])
            sys.exit(1)
        else:
            pos = match.end(0)
    return tokens