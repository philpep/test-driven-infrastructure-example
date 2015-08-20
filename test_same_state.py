import testinfra


def test_same_website_root():
    tree = {}
    for name in ("default", "production"):
        conn = testinfra.get_backend(
            name, connection="paramiko", ssh_config=".vagrant-ssh-config")
        Command = conn.get_module("Command")
        tree[name] = Command.check_output("tree /usr/share/nginx/html")

    assert tree["default"] == tree["production"]
