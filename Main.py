# This is the entrance point for the script
def main(): shell()


def shell():
    print("Starting Shell. . .")
    # TODO Need to implement shell att into settings
    get_shell_att()

    while True:
        print("> ", end="")
        lineInput = input()
        if lineInput == "exit":
            print("Exiting Shell.")
            break
        else:
            print(tokenize_line(lineInput))


def get_shell_att():
    shell_att = []
    # This is the location where default shell attributes live
    default_shell_att = ["line_num: true", "exit_command: exit"]

    try:
        # tries to open default shell attribute file, drops into except when FileNotFound
        shell_att_file = open("kitShellAtt.txt", "r")
        # grabs file contents for return
        for line in shell_att_file:
            shell_att.append(line)

    except FileNotFoundError:
        # creates file to contain shell attributes, then writes in the default values
        shell_att_file = open("kitShellAtt.txt", "x")
        for att in default_shell_att:
            shell_att_file.write(att)
        # returning the default shell attributes
        return default_shell_att

    return shell_att


# TODO this is sorta a mess, but it is MY mess
def tokenize_line(line):
    separate = True
    token_name = ""
    ret_tokens = []

    for ch in line:
        if separate:
            if ch == '"':
                separate = False
                if not token_name.strip() == "" and not token_name.isspace():
                    ret_tokens.append(Token(token_name))
                    token_name = ""
                continue
            if ch.isalnum():
                token_name += ch
            else:
                if not token_name.strip() == "" and not token_name.isspace():
                    ret_tokens.append(Token(token_name))
                    token_name = ""
                if not token_name == ' ':
                    ret_tokens.append(Token(ch))
        else:
            if ch == '"':
                tok = Token(token_name)
                tok.set_type("string")
                ret_tokens.append(tok)
                token_name = ""
                separate = True
            else:
                token_name += ch

    if not token_name.strip() == "" and not token_name.isspace():
        ret_tokens.append(Token(token_name))
    return ret_tokens


class Token:
    _name = "None"
    _type = "None"

    def __init__(self, name):
        self._name = name

    def __repr__(self):
        return f"'{self._name}', {self._type}"

    def get_name(self):
        return self._name

    def get_type(self):
        return self._type

    def set_type(self, type_of):
        self._type = type_of


if __name__ == "__main__":
    main()
