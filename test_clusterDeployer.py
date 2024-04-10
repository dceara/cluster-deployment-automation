import pathlib

import clusterDeployer


def test_resolv_conf_parse_file(tmp_path: pathlib.Path) -> None:
    def _rc(content: str | bytes) -> list[str]:
        filename = str(tmp_path / "rcfile")
        if isinstance(content, str):
            content = content.encode('utf-8')
        with open(filename, "wb") as f:
            f.write(content)
        return clusterDeployer._resolv_conf_parse_file(filename)

    assert _rc("nameserver  1.2.3.4") == ["1.2.3.4"]
    assert _rc("nameserver  1::04") == ["1::4"]
    assert _rc("nameserver 1::04") == ["1::4"]
    assert _rc("nameserver1::04") == []
    assert _rc("nameserver\t1::04") == ["1::4"]
    assert _rc("\n\tnameserver\t1::04\t\n") == ["1::4"]
    assert _rc(b"nameserver\t1::0\xca4") == []
    assert _rc(b"nameserver\t1::0\xca4\nnameserver 1.2.3.4  ") == ["1.2.3.4"]
