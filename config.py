# ==========================================#
# 메시지 보낼 시간 (시간)
set_hour = 0

# 메시지 보낼 시간 (분)
set_min = 0

# 메시지 보내기전 준비시간(분)  # 1보다 커야함
margin_minutes = 1

# API 학교 종류
sc_type = "high"

# API 학교 코드
code = "R100000822"
# ==========================================#


if set_hour < 0 or set_hour > 23:
    raise Exception("Invalid Config: set_hour")
if set_min < 0 or set_min > 59:
    raise Exception("Invalid Config: set_min")
if margin_minutes < 1:
    raise Exception("Invalid Config: margin_minutes")

# Set Ready Time
ready_hour = set_hour
ready_min = set_min - margin_minutes
if ready_min < 0:
    ready_min += 60
    ready_hour -= 1
    if ready_hour < 0:
        ready_hour += 24
