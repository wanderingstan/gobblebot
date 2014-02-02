import re, os

def read_env():
    """
    Reads settings from a .env file located in the project root
    directory and sets them as environment variables.
    Run this function first when testing locally. (Not on Heroku)
    """
    try:
        with open('.env') as f:
            content = f.read()
    except IOError:
        content = ''
        print "Could not read env file"
 
    for line in content.splitlines():
        m1 = re.match(r'\A([A-Za-z_0-9]+)=(.*)\Z', line)
        if m1:
            key, val = m1.group(1), m1.group(2)
            m2 = re.match(r"\A'(.*)'\Z", val)
            if m2:
                val = m2.group(1)
            m3 = re.match(r'\A"(.*)"\Z', val)
            if m3:
                val = re.sub(r'\\(.)', r'\1', m3.group(1))
            os.environ.setdefault(key, val)

if __name__ == "__main__":
    read_env()
