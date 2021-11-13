from py4j.java_gateway import JavaGateway

gateway  = JavaGateway()
bridge = gateway.jvm.minicpbp.bridge.EntryPoint()

java_entry_point = bridge.partialLatinSquare()

def list_int_to_java_array(l):
    arr = java_entry_point.new_array(len(l))
    for i in range(len(l)):
        arr[i] = l[i]
    return arr
