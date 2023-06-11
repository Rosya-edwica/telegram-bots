from db.config import connect_to_mysql, connect_to_postgres
from db.load import get_none_checked_skills, get_skills
from db.upload import save_all_skills_to_postgres, delete_duplicates_skills_in_mysql, s