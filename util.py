import numpy as np

def calculate_transition_matrix(speaker_data):
    speakers = list(set(speaker_data))
    num_speakers = len(speakers)

    # Create a mapping from speaker to index
    speaker_to_index = {speaker: idx for idx, speaker in enumerate(speakers)}

    # Initialize the transition matrix
    transition_matrix = np.zeros((num_speakers, num_speakers))

    # Update the transition matrix based on speaker transitions
    for i in range(1, len(speaker_data)):
        prev_speaker = speaker_data[i-1]
        curr_speaker = speaker_data[i]
        transition_matrix[speaker_to_index[prev_speaker], speaker_to_index[curr_speaker]] += 1

    return transition_matrix


def num_zeros(matrix):
    num_zero = np.prod(matrix.shape) - np.count_nonzero(matrix)

    return num_zero


def _num_zeros_list(spkr_data):
    nz_list = []
    for spkr in spkr_data:
        if len(spkr) <= 2:
            nz_list.append(0)
        else:
            matrix = calculate_transition_matrix(spkr)
            nz_list.append(int(num_zeros(matrix + np.eye(matrix.shape[0]))))
    return nz_list


def entropy(spkr_data):
    trans_matrix = calculate_transition_matrix(spkr_data)

    normed_matrix = trans_matrix / trans_matrix.sum(keepdims=True)

    _entropy = 0.0
    for i in range(normed_matrix.shape[0]):
        for j in range(normed_matrix.shape[1]):
            if normed_matrix[i, j] != 0:
                _entropy -= normed_matrix[i, j] * np.log(normed_matrix[i, j])
    return _entropy

def split_matrix(spkr_data):
    org_num_zeros = num_zeros(calculate_transition_matrix(spkr_data))
    idx_ranges = range(len(spkr_data)-1, 1, -1)

    for idx in idx_ranges:
        s1 = spkr_data[:idx]
        if len(s1) <= 2:
            return spkr_data[:idx], spkr_data[idx:]

        matrix = calculate_transition_matrix(s1)
        num_zeros_s1 = num_zeros(matrix + np.eye(matrix.shape[0]))
        # print(idx, num_zeros_s1, s1)

        # if num_zeros_s1 < org_num_zeros:
        if num_zeros_s1 == 0:
            return spkr_data[:idx], spkr_data[idx:]
        
    return None


def segmentation(x):
    speaker_data = [x]

    while not all([n == 0 for n in _num_zeros_list(speaker_data)]):
        _spkr_list = []

        for spkr_data in speaker_data:
            if _num_zeros_list([spkr_data])[0] == 0:
                _spkr_list.append(spkr_data)
            elif len(spkr_data) <= 2:
                _spkr_list.append(spkr_data)
            else:    
                s1, s2 = split_matrix(spkr_data)
                _spkr_list.append(s1)
                _spkr_list.append(s2)

        speaker_data = _spkr_list.copy()

    return speaker_data


def annotate_mono_diag(segment):
    result = []
    mono_idx, diag_idx = 0, 0
    for seg in segment:
        if len(seg) <= 2:
            result.append([f"monologue_{mono_idx:03d}"] * len(seg))
            mono_idx += 1
        elif len(list(set(seg))) == 1:
            result.append([f"monologue_{mono_idx:03d}"] * len(seg))
            mono_idx += 1
        else:
            if _num_zeros_list([seg])[0] == 0:
                entr = entropy(seg)
                result.append([f"dialogue_{diag_idx:03d}"] * len(seg))
                diag_idx += 1
            else:
                result.append([f"monologue_{mono_idx:03d}"] * len(seg))
                mono_idx += 1

    return result