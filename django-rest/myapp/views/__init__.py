from ..models import MySession
from ..models.my_user import MyUser


def check_session(request):
	if 'Authorization' not in request.headers:
		raise 'cannot verify user'
	token = request.headers['Authorization']
	session = MySession.get_by_token(token)
	return MyUser(session.uid)
