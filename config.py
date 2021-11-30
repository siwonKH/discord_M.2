# ==========================================#
# 메시지 보낼 시간 (시간)
SET_HOUR = 0

# 메시지 보낼 시간 (분)
SET_MIN = 0

# 메시지 보내기전 준비시간(분)  # 1보다 커야함
MARGIN_MINUTES = 1

# API 학교 종류
SC_TYPE = "high"

# API 학교 코드
CODE = "R100000822"

# 가사 분할 크기
PARSE_LEN = 1000
# ==========================================#


if SET_HOUR < 0 or SET_HOUR > 23:
    raise Exception("Invalid Config: set_hour")
if SET_MIN < 0 or SET_MIN > 59:
    raise Exception("Invalid Config: set_min")
if MARGIN_MINUTES < 1:
    raise Exception("Invalid Config: margin_minutes")

# Set Ready Time
READY_HOUR = SET_HOUR
READY_MIN = SET_MIN - MARGIN_MINUTES
if READY_MIN < 0:
    READY_MIN += 60
    READY_HOUR -= 1
    if READY_HOUR < 0:
        READY_HOUR += 24
