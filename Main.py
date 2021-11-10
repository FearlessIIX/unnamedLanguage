# This is the entrance point for the script
def main(): shell()


def shell():
    print("Starting Shell. . .")

    shell_att = create_att_dict(get_shell_att())
    show_line_number = False
    line_num = 1

    if shell_att["line_num"] == "true":
        show_line_number = True

    while True:
        # section for line prompt
        if show_line_number:
            print(f"[{line_num}] > ", end="")
        else:
            print("> ", end="")

        line_input = input()

        # section for exit command
        if line_input == shell_att["exit_command"]:
            print("Exited Normally, exit code: 0")
            break
        # TODO add support for changing builtin shell commands
        else:
            lex_tokens(tokenize_line(line_input))

        line_num += 1


def get_shell_att():
    shell_att = []
    # This is the location where default shell attributes live
    default_shell_att = ["line_num:true", "exit_command:exit"]

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
            shell_att_file.write(f"{att}\n")
        # returning the default shell attributes
        return default_shell_att
    shell_att_file.close()
    return shell_att


def create_att_dict(att_list):
    ret_dict = {}
    for att in att_list:
        # getting rid of newlines from parsing of attribute file
        att = att.replace("\n", "")
        ret_dict[att.split(":")[0]] = att.split(":")[1]
    return ret_dict


def tokenize_line(line):
    separate = True         # toggle for splitting tokens by spaces and symbols
    token_name = ""         # temporary storage for token names
    ret_tokens = []         # the list of tokens to be returned

    for ch in line:
        # When we are splitting tokens based upon spaces and symbols
        if separate:
            if ch == '"':
                # this if branch will invert the 'separate' variable, then append a token with the current-
                # saved name as long as the name isn't empty
                separate = False
                if not token_name.strip() == "" and not token_name.isspace():
                    ret_tokens.append(Token(token_name))
                    token_name = ""
                continue    # skipping evaluation of current character
            # appends the current character its alphanumeric
            if ch.isalnum():
                token_name += ch
            else:
                # appends a token with the current saved name as long as the name isn't empty
                if not token_name.strip() == "" and not token_name.isspace():
                    ret_tokens.append(Token(token_name))
                    token_name = ""
                # appends a token of the current character as long as it isn't a space
                if not ch == ' ':
                    ret_tokens.append(Token(ch))
        else:
            # takes in all characters until either end of line or the next double quote '"', then appends-
            # a token of those taken characters, toggles separate back to True
            if ch == '"':
                tok = Token(token_name)
                tok.set_type("string")
                ret_tokens.append(tok)
                token_name = ""
                separate = True
            else:
                token_name += ch
    # appends a token of whatever is left inside of current name unless it is empty
    if not token_name.strip() == "" and not token_name.isspace():
        ret_tokens.append(Token(token_name))
    return ret_tokens


def lex_tokens(token_list):

    for token in token_list:
        pass


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
