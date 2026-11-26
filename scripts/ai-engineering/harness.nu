def main [command: string = "health", ...arguments: string] {
    let script = ($env.FILE_PWD | path join "check.sh")
    let root = ($env.FILE_PWD | path join ".." ".." | path expand)
    cd $root
    ^bash $script $command ...$arguments
}
