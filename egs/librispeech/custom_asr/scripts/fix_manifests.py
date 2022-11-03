import lhotse
from lhotse import CutSet
import os
import tqdm

fb = lhotse.load_manifest("data/fbank/cuts_train.jsonl.gz")

missedup_fb_indices = []
correct_fb_indices = []
output_text = []

for idx, cut in enumerate(fb):
    text = fb[idx].supervisions[0].text
    print(idx, end="\r")
    if all(x.isalpha() or x.isspace() for x in text):
        output_text.append(text)
        correct_fb_indices.append(idx)
    else:
        missedup_fb_indices.append(idx)

print(f"Number of missed up files is {len(missedup_fb_indices)}. Number of Correct files is {len(correct_fb_indices)}")
output_fh = open("output_text", "w")
for line in tqdm(output_text):
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
