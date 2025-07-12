<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Peteca Scout Django Project

This is a Django web application for tracking peteca (Brazilian sport) matches with individual and team rankings.

## Project Structure
- **jogos/**: Main Django app containing all the peteca scout functionality
- **peteca_scout/**: Django project configuration
- **Templates**: HTML templates with modern, responsive design
- **Admin**: Django admin interface for data management

## Key Features
- Individual player rankings with statistics (wins, points, efficiency)
- Team/doubles rankings 
- Quarter-based filtering
- Minimum match requirements for rankings
- Admin interface for managing players, teams, and matches
- Responsive web interface with modern styling

## Development Guidelines
- Follow Django best practices
- Use Python 3.11+ features
- Maintain PEP 8 code style (max 79 characters per line)
- Use proper Django model relationships
- Include proper documentation in docstrings
- Optimize database queries with select_related/prefetch_related
- Use proper Django template inheritance

## Database Models
- **Jogador**: Individual players
- **Dupla**: Teams/doubles (many-to-many with players)
- **Partida**: Matches between two teams with scores

## Key Functions
- `ranking_individual()`: Calculate individual player rankings
- `ranking_duplas()`: Calculate team rankings  
- `filtrar_por_periodo()`: Filter matches by year/quarter
