from flaskr import db 

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, db.Sequence('user_id_seq'), primary_key=True )
    telegram_id = db.Column(db.Integer, unique=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))

    start_count = db.Column(db.Integer, default=0)
    download_count = db.Column(db.Integer, default=0)

    is_admin = db.Column(db.Boolean, default=False)
    is_owner = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<User(firstname='{self.first_name}', lastname='{self.last_name}')>"

class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, db.Sequence('user_id_seq'), primary_key=True )
    course_symbol = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(100))

    lectures = db.relationship("Lecture", back_populates = 'course', cascade="all, delete")
    refferences = db.relationship("Refference", back_populates = 'course', cascade="all, delete")
    exams = db.relationship("Exam", back_populates = 'course', cascade="all, delete")

    def __repr__(self):
        return f"<Course(name='{self.name}', course_symbol='{self.course_symbol}')>"

class Lecture(db.Model):
    __tablename__ = 'lectures'

    id = db.Column(db.Integer,  db.Sequence('user_id_seq'), primary_key=True )
    lecture_number = db.Column(db.Integer)

    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    course = db.relationship("Course", back_populates="lectures", cascade="save-update")

    documents = db.relationship("Document", back_populates = 'lecture', cascade="all, delete")
    videos = db.relationship("Video", back_populates = 'lecture', cascade="all, delete")
    youtube_links = db.relationship("YoutubeLink", back_populates = 'lecture', cascade="all, delete")

    def __repr__(self):
        return f"<Lecture(Course='{self.course.course_symbol}', No='{self.lecture_number}')>"


class Document(db.Model):
    __tablename__ = 'documents'

    id = db.Column(db.Integer,  db.Sequence('user_id_seq'), primary_key=True )
    file_name = db.Column(db.String(100))
    file_id = db.Column(db.String(300))
    file_unique_id = db.Column(db.String(300))

    lecture_id = db.Column(db.Integer, db.ForeignKey('lectures.id'))
    lecture = db.relationship("Lecture", back_populates="documents", cascade="save-update")
    def __repr__(self):
        return f"<Document(Course='{self.lecture.course.name}', lecture='{self.lecture.lecture_number}')>"

class Video(db.Model):
    __tablename__ = 'videos'

    id = db.Column(db.Integer,  db.Sequence('user_id_seq'), primary_key=True )
    file_name = db.Column(db.String(100))
    file_id = db.Column(db.String(300))
    file_unique_id = db.Column(db.String(300))

    lecture_id = db.Column(db.Integer, db.ForeignKey('lectures.id'))
    lecture = db.relationship("Lecture", back_populates="videos", cascade="save-update")
    def __repr__(self):
        return f"<Video(Course='{self.lecture.course.name}', lecture='{self.lecture.lecture_number}')>"

class YoutubeLink(db.Model):
    __tablename__ = 'youtube_links'

    id = db.Column(db.Integer,  db.Sequence('user_id_seq'), primary_key=True )
    video_title = db.Column(db.String(100))
    youtube_id = db.Column(db.String(300))
    url = db.Column(db.String(300))

    lecture_id = db.Column(db.Integer, db.ForeignKey('lectures.id'))
    lecture = db.relationship("Lecture", back_populates="youtube_links", cascade="save-update")
    def __repr__(self):
        return f"<YoutubeLink(Course='{self.lecture.course.name}', lecture='{self.lecture.lecture_number}')>"

class Refference(db.Model):
    __tablename__ = 'refferences'

    id = db.Column(db.Integer,  db.Sequence('user_id_seq'), primary_key=True )
    name = db.Column(db.String(300), nullable=False)
    file_id = db.Column(db.String(300))
    file_unique_id = db.Column(db.String(300))

    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    course = db.relationship("Course", back_populates="refferences", cascade="save-update")
    def __repr__(self):
        return f"<Refference(course='{self.course.name}', name='{self.name}')>"

class Exam(db.Model):
    __tablename__ = 'exams'

    id = db.Column(db.Integer,  db.Sequence('user_id_seq'), primary_key=True )
    file_name = db.Column(db.String(300), nullable=False)
    file_id = db.Column(db.String(300))
    file_unique_id = db.Column(db.String(300))
    file_type = db.Column(db.String(50))

    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    course = db.relationship("Course", back_populates="exams", cascade="save-update")
    def __repr__(self):
        return f"<Exam(course='{self.course.name}', name='{self.name}')>"

