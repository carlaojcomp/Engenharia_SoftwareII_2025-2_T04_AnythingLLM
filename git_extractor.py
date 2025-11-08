import subprocess
from pathlib import Path

class GitExtractor:
    def __init__(self, repo_path, output_dir="git_output"):
        self.repo = Path(repo_path)
        self.out = Path(output_dir)
        self.out.mkdir(exist_ok=True)
    
    def git(self, cmd):
        """Executa comando git"""
        result = subprocess.run(cmd, cwd=self.repo, capture_output=True, 
                              shell=True)
        # tratamento a exceção levantada, depois cheecar melhor -> Tenta UTF-8, se falhar usa latin-1 (aceita qualquer byte)
        try:
            return result.stdout.decode('utf-8')
        except UnicodeDecodeError:
            return result.stdout.decode('latin-1', errors='replace')
    
    def save(self, filename, content):
        ####Salva o conteudo conteúdo em arquivo
        (self.out / filename).write_text(content, encoding='utf-8')
        print(f"OK {filename}")
    
    def extract_all(self):
        #####Extrai tudo
        print(f" Extraindo de: {self.repo}\n")
        
        ##### Histórico completo
        self.save("commits.txt", self.git(
            'git log --all --pretty=format:"COMMIT:%H%nAUTOR:%an%nDATA:%ad%nMSG:%s%n%b%n---" --date=short --stat'
        ))
        
        ##### Mudanças de arquivos
        self.save("files.txt", self.git(
            'git log --all --name-status --pretty=format:"COMMIT:%H|%an|%ad|%s" --date=short'
        ))
        
        #### Diffs (peguei os ultimos 10k  commits, mas talvez seja necessario mais -> ajustar 
        self.save("diffs.txt", self.git('git log --all -p -n 100000'))
        
        # Estrutura de branches
        self.save("branches.txt", self.git('git log --all --graph --oneline --decorate'))
        
        # Contribuidores
        self.save("contributors.txt", self.git('git shortlog -sn --all'))
        
        # Resumo
        total = self.git('git rev-list --all --count').strip()
        first = self.git('git log --reverse --pretty=format:"%ad - %s" --date=short | head -1')
        last = self.git('git log -1 --pretty=format:"%ad - %s" --date=short')
        
        self.save("summary.txt", f"""RESUMO
Total de commits: {total}
Primeiro: {first}
Último: {last}

Arquivos gerados em: {self.out.absolute()}
""")
        
        print(f"\n Operação feita Pasta: {self.out.absolute()}")


if __name__ == "__main__":
    REPO = r"#####Caminho pro repo git local#####"
    
    extractor = GitExtractor(REPO)
    extractor.extract_all()