#!/usr/bin/python3
"""Defines the HBNB console."""
import cmd
from shlex import split
from models import storage
from datetime import datetime
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """Defines the HolbertonBnB command interpreter."""

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Amenity",
        "Place",
        "Review"
    }

    def emptyline(self):
        """Ignore empty spaces."""
        pass

    def do_quit(self, line):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, line):
        """EOF signal to exit the program."""
        print("")
        return True

    def do_create(self, line):
        """Usage: create <class> <key 1>=<value 2> <key 2>=<value 2> ...
        Create a new class instance with given keys/values and print its id.
        """
        try:
            if not line:
                raise SyntaxError()
            v_mylist = line.split(" ")

            kwargs = {}
            for i in range(1, len(v_mylist)):
                key, value = tuple(v_mylist[i].split("="))
                if value[0] == '"':
                    value = value.strip('"').replace("_", " ")
                else:
                    try:
                        value = eval(value)
                    except (SyntaxError, NameError):
                        continue
                kwargs[key] = value

            if kwargs == {}:
                obj = eval(v_mylist[0])()
            else:
                obj = eval(v_mylist[0])(**kwargs)
                storage.new(obj)
            print(obj.id)
            obj.save()

        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")

    def do_show(self, line):
        """Prints the string representation of an instance
        Exceptions:
            SyntaxError: when there is no args given
            NameError: when there is no object taht has the name
            IndexError: when there is no id given
            KeyError: when there is no valid id given
        """
        try:
            if not line:
                raise SyntaxError()
            v_mylist = line.split(" ")
            if v_mylist[0] not in self.__classes:
                raise NameError()
            if len(v_mylist) < 2:
                raise IndexError()
            objects = storage.all()
            key = v_mylist[0] + '.' + v_mylist[1]
            if key in objects:
                print(objects[key])
            else:
                raise KeyError()
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")
        except IndexError:
            print("** instance id missing **")
        except KeyError:
            print("** no instance found **")

    def do_destroy(self, line):
        """Deletes an instance based on the class name and id
        Exceptions:
            SyntaxError: when there is no args given
            NameError: when there is no object taht has the name
            IndexError: when there is no id given
            KeyError: when there is no valid id given
        """
        try:
            if not line:
                raise SyntaxError()
            v_mylist = line.split(" ")
            if v_mylist[0] not in self.__classes:
                raise NameError()
            if len(v_mylist) < 2:
                raise IndexError()
            objects = storage.all()
            key = v_mylist[0] + '.' + v_mylist[1]
            if key in objects:
                del objects[key]
                storage.save()
            else:
                raise KeyError()
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")
        except IndexError:
            print("** instance id missing **")
        except KeyError:
            print("** no instance found **")

    def do_all(self, line):
        """Usage: all or all <class> or <class>.all()
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects."""
        if not line:
            o = storage.all()
            print([o[k].__str__() for k in o])
            return
        try:
            args = line.split(" ")
            if args[0] not in self.__classes:
                raise NameError()

            o = storage.all(eval(args[0]))
            print([o[k].__str__() for k in o])

        except NameError:
            print("** class doesn't exist **")

    def do_update(self, line):
        """Updates an instanceby adding or updating attribute
        Exceptions:
            SyntaxError: when there is no args given
            NameError: when there is no object taht has the name
            IndexError: when there is no id given
            KeyError: when there is no valid id given
            AttributeError: when there is no attribute given
            ValueError: when there is no value given
        """
        try:
            if not line:
                raise SyntaxError()
            v_mylist = split(line, " ")
            if v_mylist[0] not in self.__classes:
                raise NameError()
            if len(v_mylist) < 2:
                raise IndexError()
            objects = storage.all()
            key = v_mylist[0] + '.' + v_mylist[1]
            if key not in objects:
                raise KeyError()
            if len(v_mylist) < 3:
                raise AttributeError()
            if len(v_mylist) < 4:
                raise ValueError()
            v = objects[key]
            try:
                v.__dict__[v_mylist[2]] = eval(v_mylist[3])
            except Exception:
                v.__dict__[v_mylist[2]] = v_mylist[3]
                v.save()
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")
        except IndexError:
            print("** instance id missing **")
        except KeyError:
            print("** no instance found **")
        except AttributeError:
            print("** attribute name missing **")
        except ValueError:
            print("** value missing **")

    def count(self, line):
        """count the number of instances of a class
        """
        v_counter = 0
        try:
            v_mylist = split(line, " ")
            if v_mylist[0] not in self.__classes:
                raise NameError()
            objects = storage.all()
            for key in objects:
                name = key.split('.')
                if name[0] == v_mylist[0]:
                    v_counter += 1
            print(v_counter)
        except NameError:
            print("** class doesn't exist **")

    def strip_clean(self, args):
        """strips the argument and return a string of command
        Args:
            args: input list of args
        Return:
            returns string of argumetns
        """
        sim_list = []
        sim_list.append(args[0])
        try:
            my_dict = eval(
                args[1][args[1].find('{'):args[1].find('}')+1])
        except Exception:
            my_dict = None
        if isinstance(my_dict, dict):
            new_str = args[1][args[1].find('(')+1:args[1].find(')')]
            sim_list.append(((new_str.split(", "))[0]).strip('"'))
            sim_list.append(my_dict)
            return sim_list
        new_str = args[1][args[1].find('(')+1:args[1].find(')')]
        sim_list.append(" ".join(new_str.split(", ")))
        return " ".join(i for i in sim_list)

    def default(self, line):
        """retrieve all instances of a class and
        retrieve the number of instances
        """
        v_mylist = line.split('.')
        if len(v_mylist) >= 2:
            if v_mylist[1] == "all()":
                self.do_all(v_mylist[0])
            elif v_mylist[1] == "count()":
                self.count(v_mylist[0])
            elif v_mylist[1][:4] == "show":
                self.do_show(self.strip_clean(v_mylist))
            elif v_mylist[1][:7] == "destroy":
                self.do_destroy(self.strip_clean(v_mylist))
            elif v_mylist[1][:6] == "update":
                args = self.strip_clean(v_mylist)
                if isinstance(args, list):
                    obj = storage.all()
                    key = args[0] + ' ' + args[1]
                    for k, v in args[2].items():
                        self.do_update(key + ' "{}" "{}"'.format(k, v))
                else:
                    self.do_update(args)
        else:
            cmd.Cmd.default(self, line)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
