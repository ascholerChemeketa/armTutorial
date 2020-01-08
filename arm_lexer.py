from pygments.lexer import RegexLexer, bygroups, inherit, include, words
from pygments.token import *


class CustomLexer(RegexLexer):
    name = 'ARM'
    aliases = ['arm']
    filenames = ['*.s']

    tokens = {
        'comments': [
            (r'/\*', Comment, 'multiline'),
            (r'//.*?\n', Comment),
            (r'@.*?\n', Comment),
        ],
        'multiline': [
            (r'[^*/]', Comment),
            (r'/\*', Comment, '#push'),
            (r'\*/', Comment, '#pop'),
            (r'[*/]', Comment)
        ],
        'numbers': [
            (r'#[^\s]+', Number),
            (r'0b[01]+', Number),
            (r'0x[\dABCDEFabcdef]+', Number),
            (r'-?[\d]+', Number),
        ],
        'string': [
            (r'[^"\\]+', String),
            (r'\\.', String.Escape),
            ('"', String, '#pop'),
        ],
        'root': [
            (words((
                'ADC', 'ADD', 'ADR', 'AND', 'ASR', 'B', 'BFC', 'BFI', 'BIC', 
                'BKPT', 'BL', 'BLX', 'BX', 'BXJ', 'CBZ', 'CDP', 'CDP2', 'CLREX', 
                'CLZ', 'CMN', 'CMP', 'CPS', 'DBG', 'DMB', 'DSB', 'EOR', 'ERET', 
                'HVC', 'ISB', 'IT', 'LDC', 'LDC2', 'LDM', 'LDR', 'LDRB', 'LDRBT', 'LDRD', 
                'LDRHT', 'LDRSB', 'LDRSBT', 'LDRSH', 'LDRSHT', 'LDRT', 'LSL', 'LSR', 
                'MCR', 'MCR2', 'MCRR', 'MCRR2', 'MLA', 'MLS', 'MOV', 'MOVT', 'MRC', 
                'MRC2', 'MRRC', 'MRRC2', 'MRS', 'MRS', 'MSR', 'MSR', 'MUL', 'MVN', 
                'NOP', 'ORN', 'ORR', 'PLD', 'PLDW', 'PLI', 'POP', 'PUSH', 'QADD', 'QADD8', 
                'QADD16', 'QASX', 'QDADD', 'QDSUB', 'QSAX', 'QSUB', 'QSUB8', 'QSUB16', 
                'RBIT', 'REV', 'REV16', 'REVSH', 'RFE', 'ROR', 'RRX', 'RSB', 'RSC', 
                'SADD8', 'SADD16', 'SASX', 'SBC', 'SBFX', 'SDIV', 'SEL', 'SETEND', 
                'SEV', 'SHADD8', 'SHADD16', 'SHASX', 'SHSAX', 'SHSUB8', 'SHSUB16', 
                'SMC', 'SMLAxy', 'SMLAD', 'SMLAL', 'SMLALxy', 'SMLALD', 'SMLAWy', 'SMLSD', 
                'SMLSLD', 'SMMLA', 'SMMLS', 'SMMUL', 'SMULxy', 'SMULL', 'SMULWy', 'SRS', 
                'SSAT', 'SSAT16', 'SSAX', 'SSUB8', 'SSUB16', 'STC', 'STC2', 'STM', 'STR', 
                'STRB', 'STRBT', 'STRH', 'STRHT', 'STRT', 'SUB', 'SVC', 'SYS', 'TEQ', 
                'TST', 'UADD8', 'UADD16', 'UASX', 'UBFX', 'UDIV', 'UHADD8', 'UHADD16', 
                'UHASX', 'UHSAX', 'UHSUB8', 'UHSUB16', 'UMAAL', 'UMLAL', 'UMULL', 'UQADD8', 
                'UQADD16', 'UQASX', 'UQSAX', 'UQSUB8', 'UQSUB16', 'USAD8', 'USADA8', 'USAT', 
                'USAT16', 'USAX', 'USUB8', 'USUB16', 'UXTAB', 'UXTAB16', 'UXTAH', 'UXTB', 
                'UXTH', 'UXTB16', 'WFE', 'WFI', 'YIELD',
            ), suffix=r'[EQ|NE|MI|PL|VS|VC|HI|LS|GE|LT|GT|LE|S]*\b'), Keyword),
            include('comments'),
            (words(('pc', 'lr', 'sp', 'fp'), suffix=r'\b'), Name.Builtin),
            (r'[\w_]+:', Name.Label),
            include('numbers'),
            ('"', String, 'string'),
            #(r'\w+', Name),
            (r'r\d{1,2}', Name.Builtin),
            (r',?\s+', Whitespace),
            (r'[\w_]+', Name),
            (r'\.\w+', Keyword.Namespace),
            (r'[\[\]=\{\}]', Text),
        ]
    }

