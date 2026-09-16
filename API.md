# SecureVista API Documentation

## Endpoints

### Video & Stream
- `GET /video_feed` - Real-time video stream (MJPEG)
- `POST /start_camera` - Initialize camera
- `POST /emergency_stop` - Stop system

### Analytics
- `GET /analytics` - Current analytics data
- `GET /export_analytics` - Export analytics as JSON
- `GET /analytics_dashboard` - Analytics dashboard UI
- `GET /download_logs` - Download system logs

### Control
- `POST /update_parameters` - Update detector parameters
- `POST /trigger_alert` - Manually trigger alert
- `POST /reset_stats` - Reset statistics

### Health
- `GET /health_check` - System health status
- `GET /favicon.ico` - Favicon

## Parameters

### Detector Parameters
```json
{
  "crowd_threshold": 5,
  "inactivity_threshold": 120,
  "blur_faces": true,
  "show_poses": true,
  "show_zones": false,
  "show_line_counter": true
}
```

## Response Format
All responses follow this format:
```json
{
  "stats": {
    "total_detections": 0,
    "current_people_count": 0,
    "entry_count": 0,
    "exit_count": 0,
    "crowd_alerts": 0,
    "inactivity_alerts": 0
  },
  "timestamp": "2024-12-16T12:00:00",
  "system_status": "active"
}
```

## Error Handling
- 400: Bad Request
- 500: Internal Server Error
- All errors include error message in response
