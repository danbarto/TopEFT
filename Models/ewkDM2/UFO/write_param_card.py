
__date__ = "02 Aug 2012"
__author__ = 'olivier.mattelaer@uclouvain.be'

from function_library import *

class ParamCardWriter(object):
    
    header = \
    """######################################################################\n""" + \
    """## PARAM_CARD AUTOMATICALY GENERATED BY THE UFO  #####################\n""" + \
    """######################################################################\n"""   
    
    def __init__(self, filename, list_of_parameters=None, generic=False):
        """write a valid param_card.dat"""
        
        if not list_of_parameters:
            from parameters import all_parameters
            list_of_parameters = [param for param in all_parameters if \
                                                       param.nature=='external']
        
        self.generic_output = generic
        if generic:
            self.define_not_dep_param(list_of_parameters)

        
        self.fsock = open(filename, 'w')
        self.fsock.write(self.header)
        
        self.write_card(list_of_parameters)
        self.fsock.close()
    
    def define_not_dep_param(self, list_of_parameters):
        """define self.dep_mass and self.dep_width in case that they are 
        requested in the param_card.dat"""
        from particles import all_particles
        
        self.dep_mass = [(part, part.mass) for part in all_particles \
                            if part.pdg_code > 0 and \
                                            part.mass not in list_of_parameters]
        self.dep_width = [(part, part.width) for part in all_particles\
                             if part.pdg_code > 0 and \
                                part.width not in list_of_parameters]        
    
    @staticmethod
    def order_param(obj1, obj2):
        """ order parameter of a given block """
        
        maxlen = min([len(obj1.lhacode), len(obj2.lhacode)])
    
        for i in range(maxlen):
            if obj1.lhacode[i] < obj2.lhacode[i]:
                return -1
            elif obj1.lhacode[i] == obj2.lhacode[i]:
                return 0
            else:
                return 1
        #identical up to the first finish
        if len(obj1.lhacode) > len(obj2.lhacode):
            return 1
        elif  len(obj1.lhacode) == len(obj2.lhacode):
            return 0
        else:
            return -1
        
    def write_card(self, all_ext_param):
        """ """
        
        # list all lhablock
        all_lhablock = set([param.lhablock for param in all_ext_param])
        
        # ordonate lhablock alphabeticaly
        all_lhablock = list(all_lhablock)
        all_lhablock.sort()
        # put at the beginning SMINPUT + MASS + DECAY
        for name in ['DECAY', 'MASS','SMINPUTS']:
            if name in all_lhablock:
                all_lhablock.remove(name)
                all_lhablock.insert(0, name)
        
        for lhablock in all_lhablock:
            self.write_block(lhablock)
            need_writing = [ param for param in all_ext_param if \
                                                     param.lhablock == lhablock]
            need_writing.sort(self.order_param)
            [self.write_param(param, lhablock) for param in need_writing]
            
            if self.generic_output:
                if lhablock in ['MASS', 'DECAY']:
                    self.write_dep_param_block(lhablock)

        if self.generic_output:
            self.write_qnumber()
                               
    def write_block(self, name):
        """ write a comment for a block"""
        
        self.fsock.writelines(
        """\n###################################""" + \
        """\n## INFORMATION FOR %s""" % name.upper() +\
        """\n###################################\n"""
         )
        if name!='DECAY':
            self.fsock.write("""Block %s \n""" % name)

    def write_param(self, param, lhablock):
        
        lhacode=' '.join(['%3s' % key for key in param.lhacode])
        if lhablock != 'DECAY':
            text = """  %s %e # %s \n""" % (lhacode, complex(param.value).real, param.name ) 
        else:
            text = '''DECAY %s %e \n''' % (lhacode, complex(param.value).real)
        self.fsock.write(text) 
                    


    
    def write_dep_param_block(self, lhablock):
        import cmath
        from parameters import all_parameters
        from particles import all_particles
        for parameter in all_parameters:
            exec("%s = %s" % (parameter.name, parameter.value))
        text = "##  Not dependent paramater.\n"
        text += "## Those values should be edited following analytical the \n"
        text += "## analytical expression. Some generator could simply ignore \n"
        text += "## those values and use the analytical expression\n"
        
        if lhablock == 'MASS':
            data = self.dep_mass
            prefix = " "
        else:
            data = self.dep_width
            prefix = "DECAY "

        for part, param in data:
            if isinstance(param.value, str):
                value = complex(eval(param.value)).real
            else:
                value = param.value
            
            text += """%s %s %f # %s : %s \n""" %(prefix, part.pdg_code, 
                        value, part.name, param.value)
        # If more than a particles has the same mass/width we need to write it here
        # as well
        if lhablock == 'MASS':
            arg = 'mass'
            done = [part for (part, param) in self.dep_mass]
        else:
            arg = 'width'
            done = [part for (part, param) in self.dep_width]
        for particle in all_particles:
            if particle.pdg_code <0:
                continue
            is_define = True
            if particle not in done:
                if getattr(particle, arg).lhacode[0] != particle.pdg_code:
                    is_define = False                
            if  not is_define:
                value = float(particle.get(arg).value )
                name =  particle.get(arg).name 
                text += """%s %s %f # %s : %s \n""" %(prefix, particle.pdg_code, 
                        value, particle.name, name)




        self.fsock.write(text)    
        
    sm_pdg = [1,2,3,4,5,6,11,12,13,13,14,15,16,21,22,23,24,25]
    data="""Block QNUMBERS %(pdg)d  # %(name)s 
        1 %(charge)d  # 3 times electric charge
        2 %(spin)d  # number of spin states (2S+1)
        3 %(color)d  # colour rep (1: singlet, 3: triplet, 8: octet)
        4 %(antipart)d  # Particle/Antiparticle distinction (0=own anti)\n"""
    
    def write_qnumber(self):
        """ write qnumber """
        from particles import all_particles
        import particles
        print particles.__file__
        text="""#===========================================================\n"""
        text += """# QUANTUM NUMBERS OF NEW STATE(S) (NON SM PDG CODE)\n"""
        text += """#===========================================================\n\n"""
        
        for part in all_particles:
            if part.pdg_code in self.sm_pdg or part.pdg_code < 0:
                continue
            text += self.data % {'pdg': part.pdg_code,
                                 'name': part.name,
                                 'charge': 3 * part.charge,
                                 'spin': part.spin,
                                 'color': part.color,
                                 'antipart': part.name != part.antiname and 1 or 0}
        
        self.fsock.write(text)
        
            
            
            
            
        
            
if '__main__' == __name__:
    ParamCardWriter('./param_card.dat', generic=True)
    print 'write ./param_card.dat'
    