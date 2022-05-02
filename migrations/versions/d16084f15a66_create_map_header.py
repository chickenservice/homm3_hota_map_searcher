"""create map header

Revision ID: d16084f15a66
Revises: 
Create Date: 2021-12-20 22:48:49.283061

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd16084f15a66'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'config',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('maps_location', sa.String),
    )

    op.create_table(
        'map',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String),
        sa.Column('description', sa.String),
        sa.Column('any_players', sa.Boolean),

        sa.Column('version_id', sa.Integer),
        sa.Column('map_size_id', sa.Integer),
        sa.Column('difficulty_id', sa.Integer),
        sa.Column('winning_condition_id', sa.Integer),
        sa.Column('loss_condition_id', sa.Integer),
        sa.ForeignKeyConstraint(('version_id',), ('version.id',)),
        sa.ForeignKeyConstraint(('map_size_id',), ('map_size.id',)),
        sa.ForeignKeyConstraint(('difficulty_id',), ('difficulty.id',)),
        sa.ForeignKeyConstraint(('winning_condition_id',), ('winning_condition.id',)),
        sa.ForeignKeyConstraint(('loss_condition_id',), ('loss_condition.id',)),
    )

    op.create_table(
        'player',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('map_id', sa.Integer),
        sa.Column('player_color_id', sa.Integer),
        sa.Column('team_id', sa.Integer),
        sa.ForeignKeyConstraint(('map_id',), ('map.id',)),
        sa.ForeignKeyConstraint(('player_color_id',), ('player_color.id',)),
        sa.ForeignKeyConstraint(('team_id',), ('team.id',)),
        sa.UniqueConstraint("map_id", "player_color_id", "team_id"),
    )

    version = op.create_table(
        'version',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String),
        sa.Column('version', sa.Integer),
    )

    difficulty = op.create_table(
        'difficulty',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String),
        sa.Column('difficulty', sa.Integer),
    )

    map_size = op.create_table(
        'map_size',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String),
        sa.Column('size', sa.Integer),
    )

    player_color = op.create_table(
        'player_color',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String),
    )

    town = op.create_table(
        'town',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String),
    )

    op.create_table(
        'player_town',
        sa.Column('player_id', sa.Integer, primary_key=True),
        sa.Column('town_id', sa.Integer, primary_key=True),
        sa.ForeignKeyConstraint(('town_id',), ('town.id',)),
        sa.ForeignKeyConstraint(('player_id',), ('player.id',)),
    )

    team = op.create_table(
        'team',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String),
    )

    winning_condition = op.create_table(
        'winning_condition',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String),
    )

    loss_condition = op.create_table(
        'loss_condition',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String),
    )

    op.bulk_insert(
        version,
        [
            {"name": "RoE", "version": 14},
            {"name": "AB", "version": 21},
            {"name": "SoD", "version": 28},
            {"name": "HotA", "version": 30},
            {"name": "HotA", "version": 31},
            {"name": "HotA", "version": 32},
            {"name": "Wog", "version": 51},
        ]
    )

    op.bulk_insert(
        difficulty,
        [
            {"name": "Easy", "difficulty": 0},
            {"name": "Normal", "difficulty": 1},
            {"name": "Hard", "difficulty": 2},
            {"name": "Expert", "difficulty": 3},
            {"name": "Impossible", "difficulty": 4},
        ]
    )


    op.bulk_insert(
        map_size,
        [
            {"name": "XL", "size": 144},
            {"name": "L", "size": 108},
            {"name": "M", "size": 72},
            {"name": "S", "size": 36},
        ]
    )

    op.bulk_insert(
        town,
        [
            {"name": "castle"},
            {"name": "rampart"},
            {"name": "tower"},
            {"name": "necropolis"},
            {"name": "inferno"},
            {"name": "dungeon"},
            {"name": "stronghold"},
            {"name": "fortress"},
            {"name": "conflux"},
            {"name": "neutral"},
        ]
    )

    op.bulk_insert(
        player_color,
        [
            {"name": "Red"},
            {"name": "Blue"},
            {"name": "Tan"},
            {"name": "Green"},
            {"name": "Orange"},
            {"name": "Purple"},
            {"name": "Teal"},
            {"name": "Pink"},
        ]
    )

    op.bulk_insert(
        team,
        [
            {"name": "Team 1"},
            {"name": "Team 2"},
            {"name": "Team 3"},
            {"name": "Team 4"},
            {"name": "Team 5"},
            {"name": "Team 6"},
            {"name": "Team 7"},
            {"name": "Team 8"},
        ]
    )

    op.bulk_insert(
        winning_condition,
        [
            {"name": "Standard win"},
            {"name": "Acquire artifact"},
            {"name": "Accumulate creatures"},
            {"name": "Accumulate resources"},
            {"name": "Upgrade town"},
            {"name": "Build grail"},
            {"name": "Defeat hero"},
            {"name": "Capture town"},
            {"name": "Defeat monster"},
            {"name": "Flag creatures"},
            {"name": "Flag mines"},
            {"name": "Transport artifact"},
        ]
    )

    op.bulk_insert(
        loss_condition,
        [
            {"name": "Standard loss"},
            {"name": "Lose town"},
            {"name": "Lose hero"},
            {"name": "Time expires"},
        ]
    )


def downgrade():
    op.drop_table('config')
    op.drop_table('player_town')
    op.drop_table('player')
    op.drop_table('player_color')
    op.drop_table('town')
    op.drop_table('team')
    op.drop_table('map')
    op.drop_table('difficulty')
    op.drop_table('winning_condition')
    op.drop_table('loss_condition')
    op.drop_table('version')
    op.drop_table('map_size')
