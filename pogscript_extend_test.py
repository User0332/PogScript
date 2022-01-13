import sys
import builtins
sys.path.append("modify")
from pogscript.core.parse import ModifiedParser
from pogscript.core.lex import ModifiedLexer
from pogscript.extend.types import NewType
from pogscript.modules.builtins import PogScriptBuiltinsModule

class MyType:
    pass

mylexer = ModifiedLexer()
myparser = ModifiedParser()
mydatatype = NewType("mytype", "CUSTOM_TYPE", MyType)
mybuiltins = PogScriptBuiltinsModule(builtins)

