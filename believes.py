#from bridgeJava import java_entry_point
import argparse
import math
from utility import PLSInstance
import numpy as np
import csv

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--partial-sols-filename", type=str, default=None, required=True,
                        help="Path where the partial solutions are saved to")
    parser.add_argument("--domains-filename", type=str, default=None, required=False,
                        help="Path where the variables domains are saved to")
    parser.add_argument("--domains-type", choices=['full', 'rows'], default=None,
                        help="Compute variables domains with forward checking propagator and save them in a CSV file.")
    parser.add_argument("--dim", type=int, default=None, required=True,
                        help="Problem dimension")

    args = parser.parse_args()

    leave_columns_domains = False
    save_domains = False
    if args.domains_type == 'rows':
        leave_columns_domains = True
        save_domains = True
    elif args.domains_type == 'full':
        save_domains = True


    partial_sol_filename = args.partial_sols_filename
    domains_filename = args.domains_filename

    believe_file = open("belief_" + domains_filename, "w", newline='')
    csv_writer_believe = csv.writer(believe_file, delimiter=',')
    believe_weighted_file = open("belief_w_" + domains_filename, "w", newline='')
    csv_writer_weighted_believe = csv.writer(believe_weighted_file, delimiter=',')

    with open(partial_sol_filename,mode="r") as partial_sol_file:
        with open(domains_filename, mode="r") as domains_file:

            # Count number of solutions
            count = 0
            problem = PLSInstance(n=args.dim, leave_columns_domains=leave_columns_domains)

            dim = problem.n

            # Each line is the partial assignment and the successive assignment separated by "-" character
            while True and count < math.inf:

                line_partial_sol = partial_sol_file.readline()
                if line_partial_sol is None or line_partial_sol is "":
                    break
                line_domains = domains_file.readline()

                partial_assigment = [int(i) for i in line_partial_sol.strip().split(",")]
                domains = [int(i) for i in line_domains.strip().split(",")]


                # Temporary problem instance
                tmp_problem = problem.copy()

                # Check solution len is dim * dim * dim
                assert len(partial_assigment) == dim ** 3, "len is {}".format(len(partial_assigment))

                assignment = np.asarray(partial_assigment, dtype=np.int8)
                reshaped_assign = np.reshape(assignment, (dim, dim, dim))
                dom = np.asarray(domains,dtype=np.int8)
                reshape_dom = np.reshape(dom, (dim, dim, dim))
                #print(reshaped_assign)

                tmp_problem.set_square_fromSol(reshaped_assign, reshape_dom)



                csv_writer_believe.writerow(tmp_problem.believes.reshape(-1))
                csv_writer_weighted_believe.writerow(tmp_problem.believes_w.reshape(-1))
                count +=1
                print(count)

    believe_file.close()
    believe_weighted_file.close()