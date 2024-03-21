#!/usr/bin/env bash

PS3='Select a detached session to kill:'
while true; do
    SESSIONS=$(screen -ls | grep -i detached | awk '{print $1}')
    if [ -z "$SESSIONS" ]; then
        echo 'No detached sessions to kill.'
        exit 0
    fi

    select SESSION in $SESSIONS; do
        # ignore empty strings
        [ -z "${SESSION}" ] && break
        printf "\nKilling $SESSION\n\n"
        screen -X -S $SESSION quit

        # break to refresh screen sessions
        break
    done
done
