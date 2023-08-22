#!/usr/bin/python3
"""Init console."""
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def parse(arg):
    c_bra = re.search(r"\{(.*?)\}", arg)
    brcks = re.search(r"\[(.*?)\]", arg)
    if c_bra is None:
        if brcks is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lxr = split(arg[:brcks.span()[0]])
            a_retl = [i.strip(",") for i in lxr]
            a_retl.append(brcks.group())
            return a_retl
    else:
        lxr = split(arg[:c_bra.span()[0]])
        a_retl = [i.strip(",") for i in lxr]
        a_retl.append(c_bra.group())
        return a_retl


class HBNBCommand(cmd.Cmd):
    prompt = "(hbnb) "
    __classes = {
        "BaseModel", "User", "State", "City", "Place", "Amenity", "Review"
    }

    def emptyline(self):
        pass

    def default(self, arg):
        dic_ls = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        srch = re.search(r"\.", arg)
        if srch is not None:
            abc_arg = [arg[:srch.span()[0]], arg[srch.span()[1]:]]
            srch = re.search(r"\((.*?)\)", abc_arg[1])
            if srch is not None:
                a_cmd = [abc_arg[1][:srch.span()[0]], srch.group()[1:-1]]
                if a_cmd[0] in dic_ls.keys():
                    call = "{} {}".format(abc_arg[0], a_cmd[1])
                    return dic_ls[a_cmd[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_quit(self, arg):
        """To exist the program Quit command."""
        return True

    def do_EOF(self, arg):
        """To exit the program EOF signal."""
        print("")
        return True

    def do_create(self, my_args):
        """Usage: create <class> <key 1>=<value 2> <key 2>=<value 2> ...
        Create a new class instance with given keys/values and print its id.
        """
        if len(my_args) == 0:
            print("** class a name missing **")
            return
        elif len(my_args) == 1:
            try:
                my_args = shlex.split(my_args)
                my_new_inst = eval(my_args[0])()
                my_new_inst.save()
                print(my_new_inst.id)

            except:
                print("** class doesn't exist **")
        else:
            try:
                my_args = shlex.split(my_args)
                a_name = my_args.pop(0)
                obj = eval(a_name)()
                for arg in my_args:
                    arg = arg.split('=')
                    if hasattr(obj, arg[0]):
                        try:
                            arg[1] = eval(arg[1])
                        except:
                            arg[1] = arg[1].replace('_',' ')
                        setattr(obj, arg[0], arg[1])

                obj.save()
            except:
                return
            print(obj.id)

    def do_show(self, arg):
        """Usage: show <class> <id> or <class>.show(<id>)
        Display the string representation of a class instance of a given id.
        """
        abc_arg = parse(arg)
        objdict = storage.all()
        if len(abc_arg) == 0:
            print("** missing class name  **")
        elif abc_arg[0] not in HBNBCommand.__classes:
            print("** the class name doesn't exist **")
        elif len(abc_arg) == 1:
            print("** missing id**")
        elif "{}.{}".format(abc_arg[0], abc_arg[1]) not in objdict:
            print("** instance not found **")
        else:
            print(objdict["{}.{}".format(abc_arg[0], abc_arg[1])])

    def do_destroy(self, arg):
        """Usage: destroy <class> <id> or <class>.destroy(<id>)
        Delete a class instance of a given id."""
        abc_arg = parse(arg)
        objdict = storage.all()
        if len(abc_arg) == 0:
            print("** missing class name  **")
        elif abc_arg[0] not in HBNBCommand.__classes:
            print("** the class name doesn't exist **")
        elif len(abc_arg) == 1:
            print("** missing id**")
        elif "{}.{}".format(abc_arg[0], abc_arg[1]) not in objdict.keys():
            print("** instance not found **")
        else:
            del objdict["{}.{}".format(abc_arg[0], abc_arg[1])]
            storage.save()

    def do_all(self, arg):
        """Usage: all or all <class> or <class>.all()
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects."""
        abc_arg = parse(arg)
        if len(abc_arg) > 0 and abc_arg[0] not in HBNBCommand.__classes:
            print("** the class name doesn't exist **")
        else:
            objl = []
            for obj in storage.all().values():
                if len(abc_arg) > 0 and abc_arg[0] == obj.__class__.__name__:
                    objl.append(obj.__str__())
                elif len(abc_arg) == 0:
                    objl.append(obj.__str__())
            print(objl)

    def do_count(self, arg):
        abc_arg = parse(arg)
        count = 0
        for obj in storage.all().values():
            if abc_arg[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def do_update(self, arg):
        abc_arg = parse(arg)
        objdict = storage.all()

        if len(abc_arg) == 0:
            print("** missing class name  **")
            return False
        if abc_arg[0] not in HBNBCommand.__classes:
            print("** the class name doesn't exist **")
            return False
        if len(abc_arg) == 1:
            print("** missing id**")
            return False
        if "{}.{}".format(abc_arg[0], abc_arg[1]) not in objdict.keys():
            print("** instance not found **")
            return False
        if len(abc_arg) == 2:
            print("** attribute name missing **")
            return False
        if len(abc_arg) == 3:
            try:
                type(eval(abc_arg[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(abc_arg) == 4:
            obj = objdict["{}.{}".format(abc_arg[0], abc_arg[1])]
            if abc_arg[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[abc_arg[2]])
                obj.__dict__[abc_arg[2]] = valtype(abc_arg[3])
            else:
                obj.__dict__[abc_arg[2]] = abc_arg[3]
        elif type(eval(abc_arg[2])) == dict:
            obj = objdict["{}.{}".format(abc_arg[0], abc_arg[1])]
            for k, v in eval(abc_arg[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = valtype(v)
                else:
                    obj.__dict__[k] = v
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
