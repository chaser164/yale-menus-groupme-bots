cleanup_exit() {
    local exit_status=$?
    echo "----------------------------------"
    echo ""
    exit $exit_status
}

# Set trap to run cleanup_exit on script exit
trap 'cleanup_exit' EXIT

echo "----------------------------------"
date
/home/ubuntu/yale-menus-groupme-bots/backend/.venv/bin/python /home/ubuntu/yale-menus-groupme-bots/backend/manage.py send_messages

