# Copyright (C) 2011  Bradley N. Miller
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
__author__ = 'andewscholer'

from docutils import nodes
from docutils.parsers.rst import directives
from docutils.parsers.rst import Directive
from docutils.parsers.rst import Directive
from docutils.parsers.rst.roles import set_classes

from docutils.nodes import TextElement, Inline

from sphinx.directives.code import CodeBlock, SphinxDirective
from sphinx.directives.code import CodeBlock

from runestone.common.runestonedirective import RunestoneDirective
from docutils.parsers.rst.directives.admonitions import BaseAdmonition


def setup(app):
    app.add_directive('armcode',ARMCodeBlock)
    app.add_directive('armlisting',ARMListing)
    app.add_directive('bitpattern',BitPattern)
    app.add_directive('stackdiagram',StackDiagram)
    app.add_directive('pseudo_h1',PseudoHeader) 
    app.add_directive('pseudo_h2',PseudoHeader)
    app.add_directive('pseudo_h3',PseudoHeader)
    app.add_directive('pseudo_h4',PseudoHeader)
    app.add_directive('pseudo_h5',PseudoHeader)

    return {
        'version': '1.0',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }


class arm_listing(nodes.General, nodes.Element):
    pass

class ARMListing(Directive):
    has_content = True
    required_arguments = 1
    optional_arguments = 1
    final_argument_whitespace = True

    def run(self):
        name = self.arguments[0]
        params = self.arguments[1].split(",")
        out = "<dl class='function'><dt id='" + name + "'><code class='sig-name descname'>" + name + "</code>"


        if(len(params) > 1):
            for a in params[0:-1]:
                out = out + "<em class='sig-param'>" + a + "</em>, "
            
        out = out + "<em class='sig-param'>" + params[-1] + "</em>"

        out = out + "</dt>"
        
        if(self.content):
            body = "\n".join(self.content)
            for p in params:
                if("/" in p):
                    parts = p.split("/")
                    for part in parts:
                        params.append(part)

            for p in params:
                p = p.strip()
                body= body.replace(" " + p, " <em class='param-ref'>" + p + "</em>")
            out = out + "<dd><p>" + body + "</p></dd>"

        out = out + "</dl>"

        node = nodes.raw('', out , format='html')
        return [node]


class StackDiagram(SphinxDirective):
    has_content = True
    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = True
    option_spec = {
        'no-addresses': directives.flag,
        'no-stack-pointer': directives.flag,
        'empty': directives.flag,
        'start-address': directives.unchanged_required,
        'buildup': directives.flag,
    }

    def run(self):
        start_address = 0x100000000
        if('start-address' in self.options):
            start_address = int(self.options['start-address'], 16)


        out = "<table class='stack-table'><tr>"
        out = out + "<th>Address</th>"
        out = out + "<th>Contents</th>"
        out = out + "<th></th>"
        out = out + "</tr>"

        rows = ""


        if('buildup' in self.options):
            direction_multiplier = 1
            address = start_address
        else:
            direction_multiplier = -1
            address = start_address
            # address = start_address + direction_multiplier * (len(self.content) + 1) * 4

        stack_pointer_hit = False
        if('empty' in self.options):
            stack_pointer_hit = True

        show_out_of_scope = True
        if('no-stack-pointer' in self.options):
            show_out_of_scope = False

        for line in self.content:
            parts = line.split(",")
            address = address + direction_multiplier * 4
            
            cell_class = ''
            if parts[0].strip() == '!':
                cell_class = cell_class + 'highlight'
                parts = parts[1:]

            contents = parts[0]
            note = ""

            if len(parts) > 1:
                note = parts[1]

            contents_class = ''
            if stack_pointer_hit and show_out_of_scope:  
                contents_class = contents_class + ' off-stack'
                
            if "< sp" in note:
                stack_pointer_hit = True        #udpate for next time
            
            note = note.replace("<", '<i class="fas fa-arrow-left"></i>')

            row = "<tr class=''>"
            row = row + "<td class='" + cell_class + "'>" + "0x{:08x}".format(address) + "</td>"
            row = row + "<td class='" + cell_class + contents_class + "'>" + contents + "</td>"
            row = row + "<td class='note'>" + note + "</td>"
            row = row + "</tr>"

            if('buildup' in self.options):
                rows = rows + row
            else:
                rows = row + rows

            
        start_note = ''
        if('empty' in self.options):
            start_note = '<i class="fas fa-arrow-left"></i> sp'

        if start_address == 0x100000000:
            start_address = 0x00000000

        first_row = "<tr class=''>"
        first_row = first_row + "<td class=''>" + "0x{:08x}".format(start_address) + "</td>"
        first_row = first_row + "<td class=''>" + "..." + "</td>"
        first_row = first_row + "<td class='note'>" + start_note + "</td>"
        first_row = first_row + "</tr>"

        if('buildup' in self.options):
            rows = first_row + rows
        else:
            rows = rows + first_row
        
        out = out + rows + "</table>"

        node = nodes.raw('', out , format='html')
        return [node]

        
class BitPattern(SphinxDirective):
    has_content = True
    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = True
    option_spec = {
        'inhex': directives.flag,
        'nohex': directives.flag,
        'emphasize-bits': directives.unchanged_required,
    }

    def run(self):
        bits = "".join(self.content).strip()
        # if bits[0] == '-':
        #     bits = bits[1:].rjust(32,bits[1])

        original = bits.replace(" ","")
        bits = original

        hightlights = [False for i in range(32)] 
        if('emphasize-bits' in self.options):
            emphList = self.options['emphasize-bits'].split(",")
            for e in emphList:
                eParts = e.split("-")
                if len(eParts) == 1:
                    hightlights[ int(eParts[0]) ] = True
                else:
                    for i in range(int(eParts[0]), int(eParts[1]) + 1):
                        hightlights[ i ] = True


        dashLoc = bits.find('-')

        char_size = 1
        if('inhex' in self.options):
            char_size = 8

        if dashLoc != -1:
            replaceChar = bits[dashLoc-1]
            desired_length = 32
            if('inhex' in self.options):
                desired_length = 8
            bits = bits[0:dashLoc] + "".rjust(desired_length - (len(bits) - 1), replaceChar) + bits[dashLoc + 1:]

        if('inhex' in self.options):
            bits = bin(int(bits, 16))[2:].rjust(32,'0')
        else:
            bits = bits.rjust(32,'0')


        out = "<table class='bit-table'><tr>"

        for i in range(31, -1, -1):
            out = out + "<th>" + str(i) + "</th>"

        out = out + "</tr><tr class='bitsrow'>"
    

        for i in range(31, -1, -1):
            b = bits[31 - i]
            tdclass = ""
    
            if hightlights[i]:
                tdclass = "highlight"
    
            if (i + 1) % 4 == 0:
                tdclass = tdclass + " left-border"
            if i == 0:
                tdclass = tdclass + " right-border"

            out = out + "<td class='" + tdclass + "'>" + b + "</td>"
        
        if('nohex' not in self.options):
            out = out + "</tr><tr class='hexrow'>"

            for digit in hex(int(bits, 2))[2:].rjust(8,'0'):
                digit = digit.upper()
                out = out + "<td colspan='4'>" + digit + "</td>"

        out = out + "</tr></table>"

        node = nodes.raw('', out , format='html')
        return [node]



class ARMCodeBlock(CodeBlock):
    option_spec = {
        'force': directives.flag,
        'no-simulator': directives.flag,
        'linenos': directives.flag,
        'dedent': int,
        'lineno-start': int,
        'emphasize-lines': directives.unchanged_required,
        'caption': directives.unchanged_required,
        'class': directives.class_option,
        'name': directives.unchanged,
    }

    def run(self):
        parsed = super().run()

        node = nodes.container(rawsource='')
        node.append(parsed[0])
        import uuid
        id = "armcode" + str(uuid.uuid4())
        

        code = "\n".join(self.content)

        if 'no-simulator' not in self.options:
            link = '<a href="" target="new" class="armcode" data-for="' + id + '">Try sample</a>'
            link = link + '<div style="display: none" id="' + id + '">' + code + '</div>'
            link_node = nodes.raw('', link , format='html')
            node.append(link_node)

        return [node]
        

class PseudoHeader(Directive):
    required_arguments = 1
    has_content = False
    final_argument_whitespace = True
    option_spec = {'class': directives.unchanged}
    CODE = """\
            <%(type)s %(classes)s>
               %(text)s
            </%(type)s>
            """
    def run(self):
        if 'class' not in self.options:
            self.options['classes'] = ""
        else:
            self.options['classes'] = 'class="' + self.options['class'] + '"'
        self.options['text'] = self.arguments[0]
        self.options['type'] = self.name.split("_")[1]
        
        res = self.CODE % self.options
        
        return [nodes.raw('',res , format='html')]