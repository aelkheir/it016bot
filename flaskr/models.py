from sqlalchemy import CheckConstraint
from flaskr import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, db.Sequence('user_id_seq'), primary_key=True )

    telegram_id = db.Column(db.BigInteger, unique=True)
    chat_id = db.Column(db.BigInteger, default='')
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    language = db.Column(db.String(5), default='ar', nullable=False)
    subscribed = db.Column(db.Boolean, default=True)

    start_count = db.Column(db.Integer, default=0)
    download_count = db.Column(db.Integer, default=0)

    is_admin = db.Column(db.Boolean, default=False)
    is_owner = db.Column(db.Boolean, default=False)

    settings = db.relationship("UserSetting", back_populates = 'user', cascade="all, delete")

    def __repr__(self):
        return f"<User(firstname='{self.first_name}', lastname='{self.last_name}')>"

class UserSetting(db.Model):
    __tablename__ = 'user_settings'

    id = db.Column(db.Integer, db.Sequence('user_id_seq'), primary_key=True)

    key = db.Column(db.String(50), nullable=False)
    value = db.Column(db.String(50), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates="settings", cascade="save-update")

    __table_args__ = (db.UniqueConstraint('user_id', 'key', name='user_settings_user_id_key_uc'),
    )

    def __repr__(self):
        return f"<UserSetting(key='{self.key}', value='{self.value}', user='')>"

class UserData(db.Model):
    __tablename__ = 'user_data'

    id = db.Column(db.Integer, db.Sequence('user_id_seq'), primary_key=True )

    user_id = db.Column(db.BigInteger, unique=True, nullable=False)
    data = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<UserData (user_id={self.user_id})>"

class ChatData(db.Model):
    __tablename__ = 'chat_data'

    id = db.Column(db.Integer, db.Sequence('user_id_seq'), primary_key=True )

    chat_id = db.Column(db.BigInteger, unique=True, nullable=False)
    data = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<ChatData (chat_id={self.chat_id})>"

class Conversation(db.Model):
    __tablename__ = 'conversations'

    id = db.Column(db.Integer, db.Sequence('user_id_seq'), primary_key=True )
    name = db.Column(db.String(20), nullable=False)
    key = db.Column(db.String(100), nullable=False)
    new_state = db.Column(db.Integer)

    def __repr__(self):
        return f"<Conversation (id={self.id})>"


class Semester(db.Model):
    __tablename__ = 'semesters'

    id = db.Column(db.Integer, db.Sequence('user_id_seq'), primary_key=True )
    number = db.Column(db.Integer)

    current = db.relationship("CurrentSemester", back_populates = 'semester')
    courses = db.relationship("Course", back_populates = 'semester')


    def __repr__(self):
        return f"<Semester (number={self.number})>"

class CurrentSemester(db.Model):
    __tablename__ = 'current_semester'
    CURRENT_SEMESTER_PK = '1G3S34OS29Z4'

    __table_args__ = (
            CheckConstraint(f"id = '{CURRENT_SEMESTER_PK}'", name='only_one_row'),
        )

    id = db.Column(
        db.String(50),
        default=CURRENT_SEMESTER_PK,
        primary_key=True
    )

    semester_id = db.Column(db.Integer, db.ForeignKey('semesters.id'))
    semester = db.relationship('Semester', cascade="save-update")


    def __repr__(self):
        return f"<CurrentSemester (number={self.semester.number})>"

class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, db.Sequence('user_id_seq'), primary_key=True )
    course_symbol = db.Column(db.String(50), unique=True)
    en_course_symbol = db.Column(db.String(50), default='')
    ar_name = db.Column(db.String(100))
    en_name = db.Column(db.String(100), default='')

    semester_id = db.Column(db.Integer, db.ForeignKey('semesters.id'))
    semester = db.relationship('Semester', back_populates="courses", cascade="save-update")


    lectures = db.relationship("Lecture", back_populates = 'course', cascade="all, delete")
    labs = db.relationship("Lab", back_populates = 'course', cascade="all, delete")
    assignments = db.relationship("Assignment", back_populates = 'course', cascade="all, delete")
    refferences = db.relationship("Refference", back_populates = 'course', cascade="all, delete")
    exams = db.relationship("Exam", back_populates = 'course', cascade="all, delete")

    def __repr__(self):
        return f"<Course(ar_name='{self.ar_name}', course_symbol='{self.course_symbol}')>"


class Lecture(db.Model):
    __tablename__ = 'lectures'

    id = db.Column(db.Integer,  db.Sequence('user_id_seq'), primary_key=True )
    lecture_number = db.Column(db.Integer)
    published = db.Column(db.Boolean, default=False)

    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    course = db.relationship("Course", back_populates="lectures", cascade="save-update")

    documents = db.relationship("Document", back_populates = 'lecture', cascade="all, delete")
    videos = db.relationship("Video", back_populates = 'lecture', cascade="all, delete")
    youtube_links = db.relationship("YoutubeLink", back_populates = 'lecture', cascade="all, delete")

    def __repr__(self):
        return f"<Lecture(Course='{self.course.course_symbol}', No='{self.lecture_number}')>"

class Lab(db.Model):
    __tablename__ = 'labs'

    id = db.Column(db.Integer,  db.Sequence('user_id_seq'), primary_key=True )
    lab_number = db.Column(db.Integer)
    published = db.Column(db.Boolean, default=False)

    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    course = db.relationship("Course", back_populates="labs", cascade="save-update")

    documents = db.relationship("Document", back_populates = 'lab', cascade="all, delete")
    videos = db.relationship("Video", back_populates = 'lab', cascade="all, delete")
    youtube_links = db.relationship("YoutubeLink", back_populates = 'lab', cascade="all, delete")

    def __repr__(self):
        return f"<Lab(Course='{self.course.ar_name}', No='{self.lab_number}')>"

class Assignment(db.Model):
    __tablename__ = 'assignments'

    id = db.Column(db.Integer,  db.Sequence('user_id_seq'), primary_key=True )
    assignment_number = db.Column(db.Integer)
    published = db.Column(db.Boolean, default=False)

    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    course = db.relationship("Course", back_populates="assignments", cascade="save-update")

    documents = db.relationship("Document", back_populates = 'assignment', cascade="all, delete")
    photos = db.relationship("Photo", back_populates = 'assignment', cascade="all, delete")

    def __repr__(self):
        return f"<Lab(Course='{self.course.ar_name}', No='{self.lab_number}')>"


class Document(db.Model):
    __tablename__ = 'documents'

    id = db.Column(db.Integer,  db.Sequence('user_id_seq'), primary_key=True )
    file_name = db.Column(db.String(100))
    file_id = db.Column(db.String(300))
    file_unique_id = db.Column(db.String(300))

    lecture_id = db.Column(db.Integer, db.ForeignKey('lectures.id'))
    lecture = db.relationship("Lecture", back_populates="documents", cascade="save-update")

    lab_id = db.Column(db.Integer, db.ForeignKey('labs.id'))
    lab = db.relationship("Lab", back_populates="documents", cascade="save-update")

    assignment_id = db.Column(db.Integer, db.ForeignKey('assignments.id'))
    assignment = db.relationship("Assignment", back_populates="documents", cascade="save-update")

    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'))
    exam = db.relationship("Exam", back_populates="documents", cascade="save-update")

    def __repr__(self):
        return f"<Document(Course='{self.lecture.course.ar_name}', lecture='{self.lecture.lecture_number}')>"

class Video(db.Model):
    __tablename__ = 'videos'

    id = db.Column(db.Integer,  db.Sequence('user_id_seq'), primary_key=True )
    file_name = db.Column(db.String(100))
    file_id = db.Column(db.String(300))
    file_unique_id = db.Column(db.String(300))

    lecture_id = db.Column(db.Integer, db.ForeignKey('lectures.id'))
    lecture = db.relationship("Lecture", back_populates="videos", cascade="save-update")

    lab_id = db.Column(db.Integer, db.ForeignKey('labs.id'))
    lab = db.relationship("Lab", back_populates="videos", cascade="save-update")

    def __repr__(self):
        return f"<Video(Course='{self.lecture.course.ar_name}', lecture='{self.lecture.lecture_number}')>"

class YoutubeLink(db.Model):
    __tablename__ = 'youtube_links'

    id = db.Column(db.Integer,  db.Sequence('user_id_seq'), primary_key=True )
    video_title = db.Column(db.String(100))
    youtube_id = db.Column(db.String(300))
    url = db.Column(db.String(300))

    lecture_id = db.Column(db.Integer, db.ForeignKey('lectures.id'))
    lecture = db.relationship("Lecture", back_populates="youtube_links", cascade="save-update")

    lab_id = db.Column(db.Integer, db.ForeignKey('labs.id'))
    lab = db.relationship("Lab", back_populates="youtube_links", cascade="save-update")

    def __repr__(self):
        return f"<YoutubeLink(Course='{self.lecture.course.ar_name}', lecture='{self.lecture.lecture_number}')>"

class Refference(db.Model):
    __tablename__ = 'refferences'

    id = db.Column(db.Integer,  db.Sequence('user_id_seq'), primary_key=True )
    name = db.Column(db.String(300), nullable=False)
    file_id = db.Column(db.String(300))
    file_unique_id = db.Column(db.String(300))

    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    course = db.relationship("Course", back_populates="refferences", cascade="save-update")
    def __repr__(self):
        return f"<Refference(course='{self.course.ar_name}', name='{self.name}')>"

class Exam(db.Model):
    __tablename__ = 'exams'

    id = db.Column(db.Integer,  db.Sequence('user_id_seq'), primary_key=True )
    name = db.Column(db.String(300), nullable=False)
    date = db.Column(db.DateTime(300))

    documents = db.relationship("Document", back_populates = 'exam', cascade="all, delete")

    photos = db.relationship("Photo", back_populates = 'exam', cascade="all, delete")

    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    course = db.relationship("Course", back_populates="exams", cascade="save-update")
    def __repr__(self):
        return f"<Exam(course='{self.course.ar_name}', name='{self.name}')>"


class Photo(db.Model):
    __tablename__ = 'photos'

    id = db.Column(db.Integer,  db.Sequence('user_id_seq'), primary_key=True )
    file_name = db.Column(db.String(100))
    file_id = db.Column(db.String(300))
    file_unique_id = db.Column(db.String(300))

    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'))
    exam = db.relationship("Exam", back_populates="photos", cascade="save-update")

    assignment_id = db.Column(db.Integer, db.ForeignKey('assignments.id'))
    assignment = db.relationship("Assignment", back_populates="photos", cascade="save-update")

    def __repr__(self):
        return f"<Photo(id='{self.id}')>"
