import papis
import os
import papis.utils
import papis.pick
import papis.config


class Edit(papis.commands.Command):
    def init(self):

        self.parser = self.get_subparsers().add_parser(
            "edit",
            help="Edit document information from a given library"
        )

        self.parser.add_argument(
            "document",
            help="Document search",
            nargs="?",
            default=".",
            action="store"
        )

        self.parser.add_argument(
            "-n",
            "--notes",
            help="Open notes document",
            action="store_true"
        )

    def main(self):

        documents = papis.utils.get_documents_in_lib(
            self.get_args().lib,
            self.args.document
        )
        document = self.pick(documents)

        if self.args.notes:
            self.logger.debug("Editing notes")
            if not document.has("notes"):
                self.logger.warning(
                    "The document selected has no notes attached,"\
                    " creating one..."
                )
                document["notes"] = papis.config.get("notes-name")
                document.save()
            notesPath = os.path.join(
                document.get_main_folder(),
                document["notes"]
            )
            if not os.path.exists(notesPath):
                self.logger.debug("Creating %s" % notesPath)
                open(notesPath, "w+").close()
            papis.utils.edit_file(notesPath)
        else:
            papis.utils.edit_file(document.get_info_file())
