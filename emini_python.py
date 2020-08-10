from werkzeug.security import generate_password_hash, check_password_hash

hash = generate_password_hash("bal chal")
print(hash)
ans = check_password_hash(hash, "bal hal")
print(ans)
