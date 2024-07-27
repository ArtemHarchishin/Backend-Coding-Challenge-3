from directories import Directory, FileSystem


def joins(*strings):
    return "{}\n".format("\n".join(strings))


def test_add_child_to_directory():
    # Arrange
    root = Directory("")
    # Act
    root.add_child("child")
    # Assert
    assert root == {"child": {}}


def test_directory_has_child():
    # Arrange
    root = Directory("")
    root.add_child("child")
    # Act
    name, child = root.get_child("child")
    # Assert
    assert child == {}
    assert name == "child"


def test_no_child_directory_in_the_directory():
    # Arrange
    root = Directory("")
    # Act
    name, child = root.get_child("child")
    # Assert
    assert child is None
    assert name == "child"


def test_directory_to_string():
    # Arrange
    root = Directory("directory")
    # Act
    string = str(root)
    # Assert
    assert string == "directory"


def test_backend_coding_challenge_3(capsys):
    # Arrange
    root = Directory("")
    fs = FileSystem(root)

    # Act
    fs.create("fruits")
    # Assert
    assert root == {"fruits": {}}

    # Act
    fs.create("vegetables")
    # Assert
    assert root == {"fruits": {}, "vegetables": {}}

    # Act
    fs.create("grains")
    # Assert
    assert root == {"fruits": {}, "vegetables": {}, "grains": {}}

    # Act
    fs.create("fruits/apples")
    # Assert
    assert root == {"fruits": {"apples": {}}, "vegetables": {}, "grains": {}}

    # Act
    fs.create("fruits/apples/fuji")
    # Assert
    assert root == {"fruits": {"apples": {"fuji": {}}}, "vegetables": {}, "grains": {}}

    # Act
    fs.list()
    captured = capsys.readouterr()
    # Assert
    assert captured.out == joins(
        "fruits",
        " apples",
        "  fuji",
        "grains",
        "vegetables",
    )

    # Act
    fs.create("grains/squash")
    # Assert
    assert root == {
        "fruits": {"apples": {"fuji": {}}},
        "vegetables": {},
        "grains": {"squash": {}},
    }

    # Act
    fs.move("grains/squash", "vegetables")
    # Assert
    assert root == {
        "fruits": {"apples": {"fuji": {}}},
        "vegetables": {"squash": {}},
        "grains": {},
    }

    # Act
    fs.create("foods")
    # Assert
    assert root == {
        "foods": {},
        "fruits": {"apples": {"fuji": {}}},
        "vegetables": {"squash": {}},
        "grains": {},
    }

    # Act
    fs.move("grains", "foods")
    # Assert
    assert root == {
        "foods": {
            "grains": {},
        },
        "fruits": {"apples": {"fuji": {}}},
        "vegetables": {"squash": {}},
    }

    # Act
    fs.move("fruits", "foods")
    # Assert
    assert root == {
        "foods": {
            "grains": {},
            "fruits": {"apples": {"fuji": {}}},
        },
        "vegetables": {"squash": {}},
    }

    # Act
    fs.move("vegetables", "foods")
    # Assert
    assert root == {
        "foods": {
            "grains": {},
            "fruits": {"apples": {"fuji": {}}},
            "vegetables": {"squash": {}},
        },
    }

    # Act
    fs.list()
    captured = capsys.readouterr()
    # Assert
    assert captured.out == joins(
        "foods",
        " fruits",
        "  apples",
        "   fuji",
        " grains",
        " vegetables",
        "  squash",
    )

    # Act
    fs.delete("fruits/apples")
    captured = capsys.readouterr()
    # Assert
    assert captured.out == "Cannot delete fruits/apples - fruits does not exist\n"
    # Assert
    assert root == {
        "foods": {
            "grains": {},
            "fruits": {"apples": {"fuji": {}}},
            "vegetables": {"squash": {}},
        },
    }

    # Act
    fs.delete("foods/fruits/apples")
    # Assert
    assert root == {
        "foods": {
            "grains": {},
            "fruits": {},
            "vegetables": {"squash": {}},
        },
    }

    # Act
    fs.list()
    captured = capsys.readouterr()
    # Assert
    assert captured.out == joins(
        "foods",
        " fruits",
        " grains",
        " vegetables",
        "  squash",
    )
