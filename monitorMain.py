from src.monitorMinecraft import monitor_minecraft


window_title = "Minecraft 1.21.4 - シングルプレイ"
sleep_time = 0.2
max_count = int(60 / sleep_time)     # 合計秒数/slee_time

monitor_minecraft(
    window_title,
    sleep_time,
    max_count,
    debug_mode=False
)
