from nmodl import dsl, ast
import nmodl
import sys
from glob import glob
import contextlib

dir = sys.argv[1]
driver = dsl.NmodlDriver()
with contextlib.ExitStack() as stack:
    fnames = glob(dir + "/*.mod")
    files = [stack.enter_context(open(fname)) for fname in fnames]
    trees = dict(zip([f.split("ection__")[1].split(".")[0] for f in fnames], map(driver.parse_string, (f.read() for f in files))))
lookup_visitor = dsl.visitor.AstLookupVisitor()


def get_state_complexity(program):
    return sum(len(state.definitions) for state in lookup_visitor.lookup(program, ast.AstNodeType.STATE_BLOCK))


def get_param_complexity(program):
    return sum(len(param.statements) for param in lookup_visitor.lookup(program, ast.AstNodeType.PARAM_BLOCK))


def get_assigned_complexity(program):
    return sum(len(assigned.definitions) for assigned in lookup_visitor.lookup(program, ast.AstNodeType.ASSIGNED_BLOCK))


def get_range_complexity(program):
    return len(lookup_visitor.lookup(program, ast.AstNodeType.RANGE_VAR))


def get_global_complexity(program):
    return len(lookup_visitor.lookup(program, ast.AstNodeType.GLOBAL_VAR))


def get_ion_write_complexity(program):
    return len(lookup_visitor.lookup(program, ast.AstNodeType.WRITE_ION_VAR))


def get_ion_read_complexity(program):
    return len(lookup_visitor.lookup(program, ast.AstNodeType.READ_ION_VAR))


def get_method(program):
    try:
        return list(lookup_visitor.lookup(program, ast.AstNodeType.SOLVE_BLOCK))[0].method.get_node_name()[:6]
    except IndexError:
        return ""


padl = max(len(k) for k in trees.keys())
print("\t".join(("mod".ljust(padl + 1, " "), "method", "ion_r", "ion_w", "range", "global", "state", "param", "assign")))
for fname, tree in sorted(trees.items(), key=lambda x: x[0]):
    print("\t".join(map(str, (
        fname.ljust(padl + 1, " "),
        get_method(tree),
        get_ion_read_complexity(tree),
        get_ion_write_complexity(tree),
        get_range_complexity(tree),
        get_global_complexity(tree),
        get_state_complexity(tree),
        get_param_complexity(tree),
        get_assigned_complexity(tree),
    ))))
