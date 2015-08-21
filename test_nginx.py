testinfra_hosts = ["default", "production"]


def test_package(Package):
    nginx = Package("nginx")
    assert nginx.is_installed
    assert nginx.version.startswith("1.8")


def test_service(Service):
    nginx = Service("nginx")
    nginx.is_running
    nginx.is_enabled


def test_website_root(File):
    f = File("/srv/website/hello.txt")
    assert f.exists
    assert f.content == "Hello world"
    assert f.user == "root"
    assert f.group == "root"
    assert f.mode == 644


def test_website(Command):
    output = Command.check_output(
        "curl -H 'Host: website' http://127.0.0.1/hello.txt")
    assert output == "Hello world"
