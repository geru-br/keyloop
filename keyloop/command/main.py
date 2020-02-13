from cmd import Cmd

from pprint import pprint
from pyramid.paster import bootstrap


from keyloop.models.realms import Realm


class BasePrompt(Cmd):
    intro = "Type ? to list commands"

    def do_back(self, inp):
        print()
        return True

    def help_back(self):
        print("Back to previous option. Shorthand: Ctrl-D.")

    do_EOF = do_back
    help_EOF = help_back


class RealmPrompt(BasePrompt):
    prompt = "realms> "

    def do_list(self, inp):
        realms = Realm.objects.raw({})
        pprint([r for r in realms])

    def do_add(self, inp):
        realm_name = input("Name: ")
        realm_slug = input(f"Slug [{realm_name.lower()}]: ") or realm_name.lower()
        realm_description = input("Description:  ")

        Realm(name=realm_name, slug=realm_slug, description=realm_description).update()

    def do_delete(self, inp):
        realm_slug = input(f"Slug: ")
        try:
            realm = Realm.objects.raw(dict(_id=realm_slug)).first()
        except Realm.DoesNotExist:
            print(f"Realm '{realm_slug}' not found.")
        else:
            realm.delete()

    def do_exit(self, inp):
        return True


class KeyLoopPrompt(Cmd):
    prompt = "keyloop> "
    intro = "Welcome! Type ? to list commands"

    def do_exit(self, inp):
        print("Bye")
        return True

    def help_exit(self):
        print("exit the application. Shorthand: x q Ctrl-D.")

    do_EOF = do_exit
    help_EOF = help_exit

    def do_realms(self, inp):
        RealmPrompt().cmdloop()


def main():
    with bootstrap("development.ini"):
        KeyLoopPrompt().cmdloop()
