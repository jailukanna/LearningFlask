"""
Database interaction methods for a Note class
"""
from database.core import db
from database.base_services import BaseDBService
from .models import Note
from flask import session
import uuid


class NoteDBService(BaseDBService):
    model = Note

    def get_notes_for_user(self, user_id: int) -> Note:
        """
        Get note for current user
        :param user_id:
        :return  Notes for user
        """
        return self.filter(user_id=user_id).order_by(db.desc(Note.created_on))

    def create(self, title: str, description: str, user_id: int, status: str, project_id: int) -> Note:
        """
        Create note instance
        :param project_id:
        :param status:
        :param title:
        :param description:
        :param user_id:
        :return: Note instance
        """
        note: Note = super(NoteDBService, self).new(title=title, description=description, status=status)
        note.set_user(user_id)
        note.set_uuid(uuid.uuid1().__str__())
        note.set_project(project_id)

        self.commit()

        return note

    def delete_note(self, uuid_: str):
        """
        Delete Note
        :param uuid_:
        :return:
        """
        note: Note = self.get_by_uuid(uuid_)

        db.session.delete(note)

        if note.user_id.__str__() == session['user_id'].__str__():
            self.commit()

    def change_note(self, uuid_: str, title: str, description: str, status: str, project: int) -> Note:
        """
        Change data in Note
        :param project:
        :param status:
        :param uuid_:
        :param title:
        :param description:
        :return: Note
        """
        note: Note = self.get_by_uuid(uuid_)
        note.title = title
        note.description = description
        note.status = status
        note.set_project(project)

        if note.user_id.__str__() == session['user_id'].__str__():
            self.commit()

        return note
