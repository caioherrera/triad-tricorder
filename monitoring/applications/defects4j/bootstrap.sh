apt-get update && apt-get install -y wget tar curl jq unzip git gcc

# Download OpenJDK 11 instead of 21 for Defects4J compatibility
wget https://download.java.net/java/GA/jdk11/9/GPL/openjdk-11.0.2_linux-x64_bin.tar.gz

tar xvf openjdk-11.0.2_linux-x64_bin.tar.gz

# Create directory and move Java installation
mkdir -p /tmp/java11
mv jdk-11.0.2/* /tmp/java11/

rm openjdk-11.0.2_linux-x64_bin.tar.gz
rm -rf jdk-11.0.2

# Make this Java version the system default using update-alternatives
echo "Setting up OpenJDK 11 as system default..."

# First install the alternatives (register them with the system)
update-alternatives --install /usr/bin/java java /tmp/java11/bin/java 1000
update-alternatives --install /usr/bin/javac javac /tmp/java11/bin/javac 1000
update-alternatives --install /usr/bin/jar jar /tmp/java11/bin/jar 1000
update-alternatives --install /usr/bin/javadoc javadoc /tmp/java11/bin/javadoc 1000

# Then set as default (non-interactive)
update-alternatives --set java /tmp/java11/bin/java
update-alternatives --set javac /tmp/java11/bin/javac
update-alternatives --set jar /tmp/java11/bin/jar
update-alternatives --set javadoc /tmp/java11/bin/javadoc

# Set environment variables
export JAVA_HOME=/tmp/java11
export PATH=$JAVA_HOME/bin:$PATH

# Verify installation
echo "Java installation verification:"
echo "JAVA_HOME: $JAVA_HOME"
which java
java -version

apt install -qq -y subversion perl cpanminus

mkdir /tmp/defects4j
cp setup.json /tmp/defects4j/
cp run.sh /tmp/defects4j/
cd /tmp/defects4j

git clone https://github.com/rjust/defects4j

cd defects4j
cpanm --local-lib=~/perl5 local::lib && eval $(perl -I ~/perl5/lib/perl5/ -Mlocal::lib)
cpanm --installdeps .

./init.sh

JSON_FILE="/tmp/defects4j/setup.json"

# Parse JSON and iterate over each defect
cat "$JSON_FILE" | jq -r '.defects[] | "\(.project) \(.class) \(.id)"' | while read project class id; do
    echo "Processing defect: Project=$project, Class=$class, ID=$id"
    
    # Create buggy version
    echo "Checking out buggy version..."
    /tmp/defects4j/defects4j/framework/bin/defects4j checkout -p "$project" -v "${id}b" -w "/tmp/defects4j/${project}_${id}_${class}_buggy"
    
    echo "Compiling buggy version..."
    cd "/tmp/defects4j/${project}_${id}_${class}_buggy"
    /tmp/defects4j/defects4j/framework/bin/defects4j compile

    # Create fixed version
    echo "Checking out fixed version..."
    cd /tmp/defects4j/defects4j
    /tmp/defects4j/defects4j/framework/bin/defects4j checkout -p "$project" -v "${id}f" -w "/tmp/defects4j/${project}_${id}_${class}_fixed"

    echo "Compiling fixed version..."
    cd "/tmp/defects4j/${project}_${id}_${class}_fixed"
    /tmp/defects4j/defects4j/framework/bin/defects4j compile
    
    echo "Completed processing defect: $project $class $id"
    echo "---"
done

echo "All defects processed successfully!"
