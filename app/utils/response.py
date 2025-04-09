from ninja.responses import Response

def success_response(data=None, message="Success", status=200):
    return Response({"success": True, "message": message, "data": data}, status=status)

def error_response(message="Error", status=400):
    return Response({"success": False, "message": message}, status=status)
