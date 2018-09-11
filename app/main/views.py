from flask import render_template,request,redirect,url_for,abort,flash
from . import main
from ..models import User,Comments,Pitches
from .. import db,photos
from .forms import UpdateProfile ,NewPitch, NewComment
from flask_login import login_required
import markdown2

# Views for our templates
@main.route('/')
def index():
    '''
    View function to render the index html template
    '''
    pitchess = Pitches.query.all()

    return render_template('index.html',pitchess = pitchess)


@main.route('/category/<cat_input>')
def categories(cat_input):
    '''
    view function to display the pitches of our specific category
    '''
    category_list = Pitches.query.filter_by(category = cat_input)



    return render_template('categories.html',category = category_list)


@main.route('/pitch/<int:id>')
def pitch(id):
    '''
    View function to view a pitch
    '''
    the_pitch = Pitches.query.get(id)
    if the_pitch is None:
        abort(404)

    the_pitches = markdown2.markdown(the_pitch.pitch, extras=["code-friendly", "fenced-code-blocks"])
    commentss = Comments.query.all()

    return render_template('pitch.html',pitch = pitch, the_pitch = the_pitch, comments = commentss)



@main.route('/pitch/add', methods = ['GET','POST'])
@login_required
def new_pitch():
    '''
    View function to create a new pitch
    '''
    form = NewPitch()
    if form.validate_on_submit():


        new_pitch = Pitches(title = form.title.data,pitch = form.a_pitch.data,category = form.category.data)

        new_pitch.save_pitch()
        return redirect(url_for('main.index'))

    title = "I Pitch"

    return render_template('new_pitch.html', title = title, pitch_form = form)




@main.route('/pitch/new_comment/<id>', methods = ['GET','POST'])
@login_required
def new_comments(id):
    '''
    View function to create a new comment to a pitch
    '''
    pitch = Pitches.query.filter_by(id=id)
    comment_form = NewComment()
    if comment_form.validate_on_submit():
        new_comment = Comments(comment=comment_form.comment.data)

        new_comment.save_comment()
    title = 'What do you think about that pitch? '

    return render_template('new_comment.html',title = title,form=comment_form)

@main.route('/user/<uname>')
@login_required
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))