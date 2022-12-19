import lhotse
from lhotse import CutSet
import os
import tqdm
import multiprocessing
import joblib
def get_clean_idx(fb, start, end):
    missedup_fb_indices = []
    correct_fb_indices = []
    output_text = []
    print(f"Initializing process {multiprocessing.current_process()}. This process is processing the range{start}-{end}")
    for idx in range(start, end):
        #text = fb[idx].supervisions[0].text
        text = fb[idx].supervisions[0].text.replace("<unk>", "").replace("<fil>", "").replace("<music>", "").replace("<overlap>", "").replace("<laugh>", "").replace("<noise>", "").strip()
        duration = fb[idx].duration
        if(idx % 10000 == 0):
            print(f"Process {multiprocessing.current_process()} has processed {idx - start}/{end-start}.")
        if (all(x.isalpha() or x.isspace() for x in text) and 2.3 * duration <= len(text.split())):
            output_text.append(text)
            correct_fb_indices.append(idx)
            fb[idx].supervisions[0].text = text
        else:
            missedup_fb_indices.append(idx)

    return (output_text, correct_fb_indices, missedup_fb_indices)

fb = lhotse.load_manifest("data/fbank/cuts_train.jsonl.gz")
print(f"Number of lines to process {len(fb)}")

num_workers = min(os.cpu_count(), 16)
pool = multiprocessing.Pool(num_workers)
result = list(zip(*pool.starmap(get_clean_idx, [(fb, i * int(len(fb) / num_workers), (i + 1) * int(len(fb) / num_workers)) for i in range(num_workers)])))
joblib.dump(result, "result")

missedup_fb_indices = []
correct_fb_indices = []
output_text = []

for i in range(num_workers):
    missedup_fb_indices += result[2][i]
    correct_fb_indices += result[1][i]
    output_text += result[0][i]
print()

print(f"Number of missed up files is {len(missedup_fb_indices)}. Number of Correct files is {len(correct_fb_indices)}")

output_fh = open("output_text", "w")
for line in tqdm.tqdm(output_text):
    output_fh.write(line)
    output_fh.write(os.linesep)
output_fh.close()

print(f"Writing Correct FB. File len {len(correct_fb_indices)}")
fixed_fb = CutSet()
fixed_fb = fixed_fb.from_items([fb[i] for i in correct_fb_indices])
fixed_fb.to_file("fixed_fb.jsonl.gz")


print("Writing Incorrect FB")
missedup_fb = CutSet()
missedup_fb = missedup_fb.from_items([fb[i] for i in missedup_fb_indices])
missedup_fb.to_file("missedup_fb.jsonl.gz")


