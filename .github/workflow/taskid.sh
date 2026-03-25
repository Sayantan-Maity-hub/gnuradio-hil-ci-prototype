# Submit task and capture task ID
OUTPUT=$(minus task submit my_task.task)
echo "$OUTPUT"

TASK_ID=$(echo "$OUTPUT" | grep -o '[0-9]\+' | head -n 1)

if [ -z "$TASK_ID" ]; then
    echo "Error: Could not extract TASK_ID"
    exit 1
fi

echo "Submitted task with ID: $TASK_ID"

# Poll using minus task info
while true; do
    INFO=$(minus task info $TASK_ID)

    echo "$INFO"

    if echo "$INFO" | grep -q "state=FINISHED"; then
        echo "Task $TASK_ID finished successfully"
        break
    fi

    if echo "$INFO" | grep -q "error=True"; then
        echo "Task $TASK_ID failed"
        exit 1
    fi

    echo "Task still running..."
    sleep 5
done

# Result path
RESULT_DIR="$HOME/results/task_$TASK_ID"
echo "Results available at: $RESULT_DIR"