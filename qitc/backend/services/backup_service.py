import os
import logging
import asyncio
import traceback

from datetime import datetime
from config import DB_NAME, DB_HOST, DB_PASS, DB_PORT, DB_USER

class BackupService:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    async def create_backup(self, backup_dir: str = "backups") -> str:
        """
        Создает резервную копию базы данных PostgreSQL.
        Возвращает путь к файлу резервной копии.
        """
        try:
            db_host = DB_HOST
            db_port = str(DB_PORT)  
            db_name = DB_NAME
            db_user = DB_USER
            db_pass = DB_PASS

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(backup_dir, f"{db_name}_backup_{timestamp}.dump")

            os.makedirs(backup_dir, exist_ok=True)

            command = [
                "pg_dump",
                "-U", db_user,
                "-h", db_host,
                "-p", db_port,
                "-F", "c",
                "-b",
                "-v",
                "-f", backup_file,
                db_name
            ]

            env = os.environ.copy()
            env["PGPASSWORD"] = db_pass

            process = await asyncio.create_subprocess_exec(
                *command,
                env=env,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await process.communicate()

            if process.returncode != 0:
                error_message = stderr.decode().strip()
                self.logger.warning(f"(Backup create) Backup create error: {error_message}")
                raise Exception

            self.logger.info(f"(Backup create) Backup create successuful: {backup_file}")
            return backup_file

        except Exception as e:
            self.logger.error(f"(Backup create) Error: {e}")
            self.logger.error(traceback.format_exc())
            raise

    async def restore_backup(self, backup_file: str) -> None:
        """
        Восстанавливает базу данных PostgreSQL из резервной копии.
        """
        try:
            db_host = DB_HOST
            db_port = str(DB_PORT)
            db_name = DB_NAME
            db_user = DB_USER
            db_pass = DB_PASS

            command = [
                "pg_restore",
                "--clean",
                "--if-exists",
                "--dbname", db_name,
                "--host", db_host,
                "--port", db_port,
                "--username", db_user,
                "--no-password",
                "--verbose",
                backup_file
            ]

            env = os.environ.copy()
            env["PGPASSWORD"] = db_pass

            process = await asyncio.create_subprocess_exec(
                *command,
                env=env,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await process.communicate()

            if process.returncode != 0:
                error_message = stderr.decode().strip()
                self.logger.warning(f"(Backup restore) Error backup restore: {error_message}")
                raise Exception

            self.logger.info(f"(Backup restore) Backup restore successful: {backup_file}")

        except Exception as e:
            self.logger.error(f"(Backup restore) Error: {e}")
            self.logger.error(traceback.format_exc())
            raise