from storage.database import Database
from storage.initializer import DatabaseInitializer
from services.portfolio_service import PortfolioService

def print_project(project):
    print(f"\nID: {project.id}")
    print(f"Title: {project.title}")
    print(f"Description: {project.description}")
    print(f"GitHub: {project.github_url or 'N/A'}")
    print(f"Demo: {project.demo_url or 'N/A'}")
    print(f"Date: {project.date_created or 'N/A'}")
    print(f"Featured: {'Yes' if project.featured else 'No'}")
    if project.technologies:
        print(f"Technologies: {', '.join(t.name for t in project.technologies)}")
    print()

def main():
    db = Database("portfolio.db")
    db.connect()
    DatabaseInitializer(db).initialize()
    service = PortfolioService(db)

    while True:
        print("\n--- Developer Portfolio Manager ---")
        print("1. Add Project")
        print("2. View All Projects")
        print("3. View Single Project")
        print("4. Search Projects")
        print("5. Filter by Technology")
        print("6. Edit Project")
        print("7. Delete Project")
        print("8. Export to HTML")
        print("9. Exit")
        choice = input("Choose: ").strip()

        try:
            if choice == "1":
                title = input("Title: ")
                description = input("Description: ")
                github = input("GitHub URL (optional): ")
                demo = input("Demo URL (optional): ")
                date = input("Date (YYYY-MM-DD, optional): ")
                featured_input = input("Featured? (yes/no): ").lower()
                featured = featured_input in ("yes", "y")
                techs_input = input("Technologies (comma separated): ")
                techs = [t.strip() for t in techs_input.split(",") if t.strip()]
                project = service.add_project(title, description, github, demo, date, featured, techs)
                print(f"Project added with ID {project.id}")
            elif choice == "2":
                projects = service.get_all_projects()
                if not projects:
                    print("No projects yet.")
                else:
                    for p in projects:
                        print(f"ID: {p.id} | {p.title} | Featured: {'Yes' if p.featured else 'No'}")
            elif choice == "3":
                pid = int(input("Project ID: "))
                project = service.get_project(pid)
                if project:
                    print_project(project)
                else:
                    print("Project not found.")
            elif choice == "4":
                term = input("Search term: ")
                results = service.search_projects(term)
                if results:
                    for p in results:
                        print(f"ID: {p.id} | {p.title}")
                else:
                    print("No matches.")
            elif choice == "5":
                tech = input("Technology name: ")
                results = service.filter_by_technology(tech)
                if results:
                    for p in results:
                        print(f"ID: {p.id} | {p.title}")
                else:
                    print("No projects with that technology.")
            elif choice == "6":
                pid = int(input("Project ID to edit: "))
                project = service.get_project(pid)
                if not project:
                    print("Project not found.")
                    continue
                print("Leave blank to keep current value.")
                new_title = input(f"Title [{project.title}]: ")
                new_desc = input(f"Description [{project.description}]: ")
                new_github = input(f"GitHub [{project.github_url}]: ")
                new_demo = input(f"Demo [{project.demo_url}]: ")
                new_date = input(f"Date [{project.date_created}]: ")
                featured_input = input(f"Featured? current={project.featured} (yes/no): ").lower()
                featured = featured_input in ("yes", "y") if featured_input else project.featured
                techs_input = input(f"Technologies [{', '.join(t.name for t in project.technologies)}]: ")
                techs = [t.strip() for t in techs_input.split(",") if t.strip()] if techs_input else [t.name for t in project.technologies]
                service.update_project(pid, new_title or project.title, new_desc or project.description,
                                       new_github or project.github_url, new_demo or project.demo_url,
                                       new_date or project.date_created, featured, techs)
                print("Project updated.")
            elif choice == "7":
                pid = int(input("Project ID to delete: "))
                if service.delete_project(pid):
                    print("Project deleted.")
                else:
                    print("Project not found.")
            elif choice == "8":
                filename = service.export_to_html()
                print(f"Portfolio exported to {filename}")
            elif choice == "9":
                print("Goodbye!")
                break
            else:
                print("Invalid option.")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    db.close()

if __name__ == "__main__":
    main()