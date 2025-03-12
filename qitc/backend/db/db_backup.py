import subprocess
import os
from db_config import SQLALCHEMY_DATABASE_URL

def create_backup(backup_file: str):
    """
    Создает резервную копию базы данных.
    
    :param backup_file: Путь до файла для сохранения резервной копии.
    """
    backup_dir = "/backup"
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        print(f"Backup directory created at {backup_dir}")
    
    backup_file_path = os.path.join(backup_dir, backup_file)

    try:
        # Формирование команды для создания резервной копии
        command = [
            "pg_dump", 
            f"--dbname={SQLALCHEMY_DATABASE_URL}", 
            "-F", "c",  # Формат дампа: сжатый
            "-b",  # Включение больших объектов
            "-v",  # Подробный вывод
            "-f", backup_file_path
        ]
        
        # Выполнение команды
        subprocess.run(command, check=True)
        print(f"Backup created successfully at {backup_file_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while creating backup: {e}")
        raise


def restore_backup(backup_file: str):
    """
    Восстанавливает данные из резервной копии в базу данных.
    
    :param backup_file: Путь к файлу резервной копии для восстановления.
    """
    backup_dir = "/backup"
    backup_file_path = os.path.join(backup_dir, backup_file)
    
    if not os.path.exists(backup_file_path):
        print(f"Backup file {backup_file_path} not found!")
        raise FileNotFoundError(f"Backup file {backup_file_path} not found!")

    try:
        # Формирование команды для восстановления базы данных
        command = [
            "pg_restore", 
            f"--dbname={SQLALCHEMY_DATABASE_URL}", 
            "-v",  # Подробный вывод
            backup_file_path
        ]
        
        # Выполнение команды
        subprocess.run(command, check=True)
        print(f"Database restored successfully from {backup_file_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while restoring backup: {e}")
        raise
