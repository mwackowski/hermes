
from config.logger_config import set_logger
from common.databases import read_table


logger = set_logger()


def get_knowledge_data(table: str = 'knowledge_simple') -> str:
    logger.info(f'Reading knowledge base from {table}...')
    df = read_table(table)
    data = '\n'.join(df.content)
    logger.info(f"Data retrieved: {data or 'No data'}")
    return data