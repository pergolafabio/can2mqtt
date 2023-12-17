import argparse
import asyncio
import logging
import coloredlogs
import can2mqtt
import can


def main():
    logging.getLogger("canopen.pdo.base").level = logging.WARNING
    # patch bug in canopen-async
    asyncio.iscouroutine = asyncio.iscoroutine

    parser = argparse.ArgumentParser(
        prog="can2mqtt",
        description="CAN to MQTT converter",
    )
    parser.add_argument("-s", "--mqtt-server")
    parser.add_argument("-i", "--interface")
    parser.add_argument("-c", "--channel")
    parser.add_argument("-b", "--bitrate")
    parser.add_argument("-l", "--log-level", default="INFO")
    parser.add_argument("-t", "--mqtt-topic-prefix")
    args = parser.parse_args()

    config_overrides = {
        k: v for k, v in vars(args).items() if v is not None
    }

    config = can.util.load_config(config=config_overrides)

    coloredlogs.DEFAULT_LOG_FORMAT = (
        "%(asctime)s %(hostname)s %(name)-18s %(levelname)s %(message)s"
    )
    coloredlogs.DEFAULT_LEVEL_STYLES.update(
        {"debug": {"color": 8}, "info": {"color": "green"}}
    )
    coloredlogs.install(level=args.log_level)

    asyncio.run(can2mqtt.start(**config))
