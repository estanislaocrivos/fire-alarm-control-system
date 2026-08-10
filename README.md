# Bare-metal C project template for multi-platform embedded development

## Repository structure

### File organization

- `src/`: Contains the source code files.
- `inc/`: Contains the header files.
- `external/`: Submodule containing shared libraries files.
- `test/`: Contains the unit and integration tests.

## Development and testing locally

### [Ceedling](https://www.throwtheswitch.org/ceedling)

Unit testing framework for C. Requires [Ruby](#additional-tools).

```bash
gem install ceedling
```

### [clang-format](https://clang.llvm.org/get_started.html)

Automatic code formatting for C source and header files.

```bash
sudo apt install clang-format
```

### [cppcheck](https://cppcheck.sourceforge.io/)

Static analysis tool for detecting bugs and undefined behavior.

```bash
sudo apt install cppcheck
```

### [pre-commit](https://pre-commit.com)

Runs clang-format, cppcheck and commit message checks automatically on each commit. After installing, enable the hooks:

```bash
pip install pre-commit
pre-commit install --install-hooks -t pre-commit -t commit-msg
```
