from django.shortcuts import render

# Create your views here.
def index_ssr(request):
  strr = "i am index.html"
  ctx = {
    "index_ssr": strr
  }
  return render(request, "index.html", ctx)


def chat_ssr(request):
  strr = "i am chat.html"
  ctx = {
    "chat_ssr": strr
  }
  return render(request, "index.html", ctx)


def chat_room_ssr(request, room):
  strr = f"i am chat.html {room}"
  tags = f"<p>{strr}</p>"
  ctx = {
    "chat_room_ssr": tags
  }
  return render(request, "index.html", ctx) 

# Create your views here.
