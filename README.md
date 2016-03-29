Arch_Lab
======

Lab assignment for Architectures in university. You probably have zero interest in this. Python.

### Now viewing lab2. See lab1 in branches.

**TESTING WITH STRINGIO COULD NOT BE IMPLEMENTED**
...because pickle requires binary file mode (yes, in Python 3 it's **no longer makes sense only for Шindoшs!**).

Dancing around that (as in using old pickle protocol) justs so tests can be implemented in this specific way would be not elegant nor smart. I won't do it.

By the way, because of the same restraint (pickle needs byte mode, but other methods need text mode) with clauses can't be moved out of backends in a way that would keep code nice.

All that taken into account,

# I implemented tests using tempfile.
